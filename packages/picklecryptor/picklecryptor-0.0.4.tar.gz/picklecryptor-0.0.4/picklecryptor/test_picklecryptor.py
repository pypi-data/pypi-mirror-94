from . import PickleCryptor, EncryptionType, CompressionType

def test_picklecryptor_end_to_end():
    ''' this test goes through an does every combination of encryption type with every compression type and allowed password length '''
    d = {'a': 1234}
    s = {1, 2, 3, 4, 9595, 32}
    t = ('A', 2, 'CCCLOL')
    for encryption_type in EncryptionType:
        for compression_type in CompressionType:
            for i in range(1, 33):
                pw = 'a' * i
                print (f"Testing: {encryption_type}, {compression_type}, i={i}, pw={pw}")
                p = PickleCryptor(pw, encryption_type, compression_type)
                assert p.deserialize(p.serialize(d)) == d
                assert p.deserialize(p.serialize('lolcats')) == 'lolcats'
                assert p.deserialize(p.serialize(t)) == t
                assert p.deserialize(p.serialize(s)) == s