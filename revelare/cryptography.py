import numpy as np


def rc4_ksa(perm: np.ndarray, key: np.ndarray):
    if len(key) == 0:
        return
    j = 0
    # Modifikasi: masing-masing elemen pada array diswap minimal 10 kali
    for i in range(256 * 10):
        j += perm[i % 256] + key[i % len(key)]
        j %= 256
        perm[i % 256], perm[j] = perm[j], perm[i % 256]

        # Modifikasi LFSR
        key[i % len(key)] = key[i % len(key)] ^ key[(i - 1) % len(key)]


def rc4_prga(perm: np.ndarray, length: int) -> dict:
    res = []
    i = 0
    j = 0
    t = 0
    for idx in range(length):
        i = idx % 256
        j = (j + perm[i]) % 256
        perm[i], perm[j] = perm[j], perm[i]
        t = (perm[i] + perm[j]) % 256
        res.append(perm[t])
    return {"latest-i": i, "latest-j": j, "latest-t": t, "keystream": np.array(res)}


def str_to_ndarray(string: str) -> np.ndarray:
    return np.array(list(map(ord, string)), dtype=np.uint8)


def crypt(message: str, key: str) -> dict:
    return crypt_byte(str_to_ndarray(message), str_to_ndarray(key))


def crypt_byte(message: np.ndarray, key: np.ndarray) -> dict:
    # Initiate permutation
    perm = np.array([i for i in range(256)])
    rc4_ksa(perm, key)

    copy_perm = np.array([perm[i] for i in range(256)])

    # Generate keystream of length len(message)
    keystream_obj = rc4_prga(perm, len(message))
    # Pad the array to be divisible by 8
    lenpad = (-len(message) % 8)
    if(lenpad > 0):
        message = np.append(message, [0 for i in range(lenpad)])
    keystream_padded = rc4_prga(copy_perm, len(message))["keystream"]

    res = []
    for idx in range(len(message) // 8):
        # Buat matrix 8*8 dari message
        temp = [[message[8 * idx + i]] for i in range(8)]
        message_matrix = np.unpackbits(np.array(temp, dtype=np.uint8), axis=1)

        # Buat matrix 8*8 dari keystream
        temp = [[keystream_padded[8 * idx + i]] for i in range(8)]
        keystream_matrix = np.unpackbits(np.array(temp, dtype=np.uint8), axis=1)

        # Jumlahkan transpose dari message_matrix, keystream_matrix, dan transpose dari keystream_matrix
        temp = np.array([[message_matrix[j][i] ^ keystream_matrix[i][j] ^ keystream_matrix[j][i] for j in range(8)] for i in range(8)])
        result_matrix = np.packbits(temp)
        for i in range(8):
            res.append(result_matrix[i])

    return {
        "keystream_obj": keystream_obj,
        "keystream": "".join(map(chr, keystream_obj["keystream"])),
        "perm": perm,
        "result": "".join(map(chr, res)),
        "result_byte": np.array(res)
    }
