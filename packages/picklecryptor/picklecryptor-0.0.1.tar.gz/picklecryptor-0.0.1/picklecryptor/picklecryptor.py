'''
The main implementation file for PickleCryptor
'''

import base64
import enum
import pickle
import typing
import zlib

from Crypto.Cipher import AES, Salsa20
from Crypto.Util.Padding import pad, unpad

class EncryptionType(enum.Enum):
    ''' Enum representing the types of encryption PickleCryptor can perform '''
    NONE = enum.auto() #: Use no encryption
    AES_ECB = enum.auto()
    SALSA_20 = enum.auto()

class CompressionType(enum.Enum):
    ''' Enum representing the types of compression PickleCryptor can perform '''
    NONE = enum.auto()
    ZLIB_DEFAULT = enum.auto()
    ZLIB_BEST_SPEED = enum.auto()
    ZLIB_BEST_COMPRESSION = enum.auto()
    ZLIB_NO_COMPRESSION = enum.auto()

def _repeat_to_length(string_to_expand: typing.Union[bytes, str], length:int) -> typing.Union[bytes, str]:
    ''' Repeats the given string to get to the given length '''
    return (string_to_expand * (int(length / len(string_to_expand)) + 1))[:length]

class PickleCryptor:
    def __init__(self,
                 password:str='',
                 encryption:EncryptionType=EncryptionType.AES_ECB,
                 compression:CompressionType=CompressionType.ZLIB_DEFAULT,
                 pickle_module=pickle):
        '''
        Creates an object that can be used to serialize/deserialize python objects.
            When serializing/unserializting the given encryption and compression will be
            used along with the given pickle_module and password.

        Arguments:
            password: A key to use to encrypt/decrypt the data
            encryption: A member of EncryptionType denoting what type of encryption to perform
            compression: A member of CompressionType denoting what type of compression to perform
            pickle_module: The serialization module to use. Must have .dumps and .loads methods similar to pickle.
        '''

        if len(password) < 1 and self._encryption != EncryptionType.NONE:
            raise ValueError("Password should be longer than empty for encryption.")

        # if password is not divisible by block size, lengthen to fill the next block
        password = password.encode()

        self._password = password
        self._encryption = encryption
        self._pickle_module = pickle_module
        self._compression = compression

        encryption_module = None
        if self._encryption == EncryptionType.AES_ECB:
            encryption_module = AES
        elif self._encryption == EncryptionType.SALSA_20:
            encryption_module = Salsa20

        if encryption_module:
            for possible_block_size in [k for k in getattr(encryption_module, 'key_size') if k % getattr(encryption_module, 'block_size', 1) == 0]:
                if len(self._password) <= possible_block_size:
                    self._encryption_block_size = possible_block_size
                    self._password = _repeat_to_length(self._password, self._encryption_block_size)
                    break
            else:
                raise ValueError(f"For {encryption.name} encryption, the password was too long. It could not fit in a supported key size. Max key size: {max(AES.key_size)}. It's size was: {len(self._password)}.")

        # this must be done after self._password is fully setup
        if self._encryption == EncryptionType.AES_ECB:
            self._aes = AES.new(self._password, AES.MODE_ECB)

    def _ensure_is_bytes(self, data:bytes) -> None:
        ''' Takes in the given data field and with raise TypeError if it is not a bytes object '''
        if not isinstance(data, bytes):
            raise TypeError(f"data should be of type bytes. It is of type: {type(data)}")

    def _encrypt(self, data:bytes) -> bytes:
        '''
            Returns the encrypted version of the data. See _decrypt() for the other direction.
            Uses the originally given encryption type and password.
        '''
        self._ensure_is_bytes(data)

        if self._encryption == EncryptionType.NONE:
            pass
        elif self._encryption == EncryptionType.AES_ECB:
            data =self._aes.encrypt(pad(data, self._encryption_block_size))
        elif self._encryption == EncryptionType.SALSA_20:
            cipher = Salsa20.new(key=self._password)
            data = cipher.nonce + cipher.encrypt(data)
        else:
            raise ValueError(f"Unsupported encryption type: {self._encryption}")
        return data

    def _decrypt(self, data:bytes) -> bytes:
        '''
            Returns the decrypted version of the data. See _encrypt() for the other direction.
            Uses the originally given encryption type and password.
        '''
        self._ensure_is_bytes(data)

        if self._encryption == EncryptionType.NONE:
            pass
        elif self._encryption == EncryptionType.AES_ECB:
            data = unpad(self._aes.decrypt(data), self._encryption_block_size)
        elif self._encryption == EncryptionType.SALSA_20:
            nonce = data[:8]
            secret = data[8:]
            data = Salsa20.new(self._password, nonce).decrypt(secret)
        else:
            raise ValueError(f"Unsupported encryption type: {self._encryption}")
        return data

    def _compress(self, data:bytes) -> bytes:
        '''
            Returns the compressed version of the data. See _decompress() for the other direction.
            Uses the originally given compression type.
        '''
        self._ensure_is_bytes(data)

        if self._compression == CompressionType.NONE:
            pass
        elif self._compression == CompressionType.ZLIB_DEFAULT:
            data = zlib.compress(data, zlib.Z_DEFAULT_COMPRESSION)
        elif self._compression == CompressionType.ZLIB_BEST_SPEED:
            data = zlib.compress(data, zlib.Z_BEST_SPEED)
        elif self._compression == CompressionType.ZLIB_BEST_COMPRESSION:
            data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
        elif self._compression == CompressionType.ZLIB_NO_COMPRESSION:
            data = zlib.compress(data, zlib.Z_NO_COMPRESSION)
        else:
            raise ValueError(f"Unsupported compression type: {self._compression}")

        return data

    def _decompress(self, data:bytes) -> bytes:
        '''
            Returns the uncompressed version of the data. See _compress() for the other direction.
            Uses the originally given compression type.
        '''
        self._ensure_is_bytes(data)

        if self._compression == CompressionType.NONE:
            pass
        elif self._compression in (CompressionType.ZLIB_DEFAULT,
                                   CompressionType.ZLIB_BEST_SPEED,
                                   CompressionType.ZLIB_BEST_COMPRESSION,
                                   CompressionType.ZLIB_NO_COMPRESSION):
            data = zlib.decompress(data)
        else:
            raise ValueError(f"Unsupported compression type: {self._compression}")

        return data

    def serialize(self, obj:typing.Any) -> bytes:
        '''
        Takes the given object, serializes it using the given pickle module.
            Then compresses it using the given compression type.
            Then encrypts it using the given encryption type.
            Returns the encrypted/compressed/serialized data.
        '''
        pickle_data = self._pickle_module.dumps(obj)
        compressed_data = self._compress(pickle_data)
        encrypted_data = self._encrypt(compressed_data)
        return encrypted_data

    def deserialize(self, data:bytes) -> typing.Any:
        '''
        Takes the given data, decrypts it using the given encryption type.
            Then uncompresses it using the given compression type.
            Then deserializes it using the given pickle module.
            Returns the final object.
        '''
        self._ensure_is_bytes(data)

        decrypted_data = self._decrypt(data)
        uncompressed_data = self._decompress(decrypted_data)
        obj = self._pickle_module.loads(uncompressed_data)
        return obj

if __name__ == '__main__':
    p = PickleCryptor('test123', EncryptionType.SALSA_20, CompressionType.ZLIB_BEST_COMPRESSION)
    self = p
