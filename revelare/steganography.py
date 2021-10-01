from typing import Tuple
import numpy as np
from icecream import ic


def inject_message(obj: np.ndarray, message: np.ndarray, filename: str, random=False, seed=42) -> np.ndarray:
    # check object validity
    capacity = obj.size // 8
    if capacity < 5 + len(filename) + 1 + len(message):
        raise ValueError("object size too small")

    original_shape = obj.shape
    stego_obj = obj.flatten()

    # get bits from message
    message_bits = np.unpackbits(message)

    # get bits from message length
    length_bits = np.unpackbits(np.array([len(message)], dtype=np.uint32).view(np.uint8))

    # get bits from filename
    filename += "$"
    filename_bits = np.unpackbits(np.array(list(map(ord, filename)), dtype=np.uint8))

    # if not random, set seed to zero
    if not random:
        seed = 0

    # get bits from seed
    seed_bits = np.unpackbits(np.array([seed], dtype=np.uint8))

    # append info together
    stego_obj[:32] = (stego_obj[:32] & ~1) | length_bits
    stego_obj[32:40] = (stego_obj[8:16] & ~1) | seed_bits
    stego_obj[40 : 40 + len(filename_bits)] = (stego_obj[40 : 40 + len(filename_bits)] & ~1) | filename_bits

    # LSB change order
    order = np.arange(start=40 + len(filename_bits), stop=40 + len(filename_bits) + 8 * len(message))
    if random:
        np.random.seed(seed)
        np.random.shuffle(order)
    ic(order)

    # set each LSB to message bit
    stego_obj[order] = (stego_obj[order] & ~1) | message_bits

    stego_obj = stego_obj.reshape(original_shape)
    return stego_obj


def extract_message(obj: np.ndarray) -> Tuple[str, np.ndarray]:
    obj = obj.flatten()

    # pack LSB to array
    lsb_array = np.array([bit & 1 for bit in obj])

    # get message length
    message_length = np.sum(
        np.packbits(lsb_array[:32].reshape((-1, 4, 8))[:, ::-1]) * np.array([1 << 24, 1 << 16, 1 << 8, 1 << 0])
    )

    # get seed
    seed = np.packbits(lsb_array[32:40])[0]

    # get filename
    filename = ""
    pos = 40
    cc = chr(np.packbits(lsb_array[pos : pos + 8])[0])
    while cc != "$":
        filename += cc
        pos += 8
        cc = chr(np.packbits(lsb_array[pos : pos + 8])[0])

    pos += 8

    # detect if random
    random = seed != 0

    # get order
    order = np.arange(start=pos, stop=pos + 8 * message_length)
    if random:
        np.random.seed(seed)
        np.random.shuffle(order)

    message_bits = lsb_array[order]
    message = np.packbits(message_bits.reshape((len(message_bits) // 8, 8)))

    return filename, message
