import numpy as np
import copy


def rc4_ksa(perm: np.array, key: np.array):
    j = 0
    for i in range(256):
        j += perm[i] + key[i % len(key)]
        j %= 256
        perm[i], perm[j] = perm[j], perm[i]


def rc4_prga(perm: np.array, length: int) -> np.array:
    perm_cpy = copy.deepcopy(perm)
    res = []
    j = 0
    for idx in range(length):
        i = idx % 256
        j = (j + perm_cpy[i]) % 256
        perm_cpy[i], perm_cpy[j] = perm_cpy[j], perm_cpy[i]
        t = (perm_cpy[i] + perm_cpy[j]) % 256
        res.append(perm_cpy[t])
    return np.array(res)


def crypt(message: np.array, key: np.array) -> np.array:
    # Initiate permutation
    perm = np.array([i for i in range(256)])
    rc4_ksa(perm, key)

    # Generate keystream of length len(message)
    keystream = rc4_prga(perm, len(message))

    res = []
    for i in range(len(message)):
        res.append(message[i] ^ keystream[i])
    return np.array(res)


"""
message = "TES"
key = "TES"
print(
    crypt(
        np.array(list(map(ord, message)), dtype=np.uint8), np.array(list(map(ord, key)), dtype=np.uint8)
    )
)
"""
