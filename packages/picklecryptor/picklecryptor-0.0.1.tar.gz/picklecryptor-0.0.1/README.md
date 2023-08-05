![Run tests](https://github.com/csm10495/picklecryptor/workflows/Run%20tests/badge.svg) [![PyPI version](https://badge.fury.io/py/picklecryptor.svg)](https://badge.fury.io/py/picklecryptor)

# PickleCryptor

A simple library for serializing / compressing / encrypting Python objects all in one function.

# Installation
```
pip install picklecryptor
```

# Simple Usage Example
```
>>> from picklecryptor import *
>>> p = PickleCryptor(password='hello world')
>>> d = {'a' : 'hi'}
>>> s = p.serialize(d)
>>> print(s)
b'{\xa9\xbc\x8e]N\xf1\xa1\xefk\xeb5\x99\\\xd1\xca\x01\x8d6\x81\x12 \x80\xeew=\xeeq\xa3\xc9B\x08'
>>> print(p.deserialize(s))
{'a': 'hi'}
```

In this example we create a PickleCryptor object that will use the given password for encryption/decryption. Using the default params for the encryption/compression parameters leads to AES ECB encryption along winh zlib compression using it's default setting.

Some non-default types of compression and encryption are natively supported. Check the docs for more information.

See [https://csm10495.github.io/picklecryptor/](https://csm10495.github.io/picklecryptor/) for full API documentation.

## License
MIT License