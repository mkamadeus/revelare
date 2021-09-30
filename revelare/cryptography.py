import numpy as np


def rc4_ksa(perm: np.array, key: np.array):
    if len(key) == 0:
        return
    j = 0
    for i in range(256):
        j += perm[i] + key[i % len(key)]
        j %= 256
        perm[i], perm[j] = perm[j], perm[i]


def rc4_prga(perm: np.array, length: int) -> dict:
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


def crypt(messageStr: str, keyStr: str) -> dict:
    # Convert to np array
    message = np.array(list(map(ord, messageStr)), dtype=np.uint8)
    key = np.array(list(map(ord, keyStr)), dtype=np.uint8)
    
    # Pad the array to be divisible by 8
    # lenpad = (-len(messageStr) % 8)
    # if(lenpad > 0):
    #     message = np.append(message, [0 for i in range(lenpad)])
    # print(message)
    return crypt_byte(message, key)


def crypt_byte(message: np.array, key: np.array) -> dict:
    # Initiate permutation
    perm = np.array([i for i in range(256)])
    rc4_ksa(perm, key)

    # Generate keystream of length len(message)
    keystream_obj = rc4_prga(perm, len(message))

    res = []
    for i in range(len(message)):
        res.append(message[i] ^ keystream_obj["keystream"][i])

    return {
        "keystream_obj": keystream_obj,
        "keystream": "".join(map(chr, keystream_obj["keystream"])),
        "perm": perm,
        "result": "".join(map(chr, res)),
        "result_byte": np.array(res)
    }
