import numpy as np
from icecream import ic


def inject_message(obj: np.ndarray, message: np.ndarray, random=False, seed=42) -> np.ndarray:
    original_shape = obj.shape
    stego_obj = obj.flatten()

    # get bits from message
    message_bits = np.unpackbits(message)

    ic(len(message))

    # get bits from message length
    length_bits = np.unpackbits(np.array([len(message)], dtype=np.uint32).view(np.uint8))

    # if not random, set seed to zero
    if not random:
        seed = 0

    # get bits from seed
    seed_bits = np.unpackbits(np.array([seed], dtype=np.uint8))

    # append info together
    stego_obj[:32] = (stego_obj[:32] & ~1) | length_bits
    stego_obj[32:40] = (stego_obj[8:16] & ~1) | seed_bits

    ic(stego_obj[:32])
    ic(stego_obj[32:40])

    # LSB change order
    order = np.arange(start=5 * 8, stop=(5 + len(message)) * 8)
    if random:
        np.random.seed(seed)
        np.random.shuffle(order)
    ic(order)

    # set each LSB to message bit
    stego_obj[order] = (stego_obj[order] & ~1) | message_bits

    stego_obj = stego_obj.reshape(original_shape)
    return stego_obj


def extract_message(obj: np.ndarray) -> np.ndarray:
    obj = obj.flatten()

    # pack LSB to array
    lsb_array = np.array([bit & 1 for bit in obj])

    # get message length
    message_length = np.sum(
        np.packbits(lsb_array[:32].reshape((-1, 4, 8))[:, ::-1]) * np.array([1 << 24, 1 << 16, 1 << 8, 1 << 0])
    )

    # get seed
    seed = np.packbits(lsb_array[32:40])[0]

    ic(message_length)
    ic(seed)

    # detect if random
    random = seed != 0

    # get order
    order = np.arange(start=5 * 8, stop=(5 + message_length) * 8)
    if random:
        np.random.seed(seed)
        np.random.shuffle(order)
    ic(order)

    message_bits = lsb_array[order]
    message = np.packbits(message_bits.reshape((len(message_bits) // 8, 8)))

    return message


def get_capacity(obj: np.ndarray):
    object_size = obj.shape
    lsb_count = np.product(object_size)
    byte_count = lsb_count // 8
    return byte_count


def is_valid(obj: np.ndarray):
    capacity = get_capacity(obj)
    return capacity > 5


def get_message_capacity(obj: np.ndarray):
    capacity = get_capacity(obj)

    # subtracting by 5 since 5 first bytes are used for stego-meta
    capacity -= 5
    return capacity
