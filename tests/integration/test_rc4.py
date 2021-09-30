from revelare.cryptography import crypt
import pytest


def nb_char_diff(str1, str2):
    res = 0
    idx = 0
    while(idx < len(str1) and idx < len(str2)):
        if(str1[idx] != str2[idx]):
            res += 1
        idx += 1
    while(idx < len(str1)):
        if(str1[idx] != chr(0)):
            res += 1
        idx += 1
    while(idx < len(str2)):
        if(str2[idx] != chr(0)):
            res += 1
        idx += 1
    return res


@pytest.mark.parametrize(
    "message1,message2,key",
    [
        ("H4lo Dunia", "Halo Dunia", "Kunci Testing"),
        ("Tes tes 123", "Tes tes 12E", ""),
    ],
)
def test_flip_byte_attack(message1, message2, key):
    assert nb_char_diff(message1, message2) == 1
    result1 = crypt(message1, key)["result"]
    result2 = crypt(message2, key)["result"]
    assert nb_char_diff(result1, result2) <= 8


@pytest.mark.parametrize(
    "filename,key",
    [
        ("./mocks/crypt/NewClass.class", "Kunci Testing"),
        ("./mocks/crypt/requirements.txt", "Kriptografi"),
    ],
)
def test_encrypt_equal_decrypt(filename, key):
    with open(filename, "rb") as file:
        isi = file.read()
        message = ''.join(map(chr, isi))
        encrypted = crypt(message, key)["result"]
        decrypted = crypt(encrypted, key)["result"]
        assert nb_char_diff(message, decrypted) == 0



