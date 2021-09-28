import numpy as np


def inject_message(
    obj: np.ndarray, message: np.ndarray, random=False, seed=42
) -> np.ndarray:
    original_shape = obj.shape
    stego_obj = obj.flatten()

    # get bits from message
    message_bits = np.unpackbits(message)

    # get bits from message length
    length_bits = np.unpackbits(np.array([len(message)], dtype=np.uint8))

    # if not random, set seed to zero
    if not random:
        seed = 0

    # get bits from seed
    seed_bits = np.unpackbits(np.array([seed], dtype=np.uint8))

    # append info together
    stego_obj[:8] = (stego_obj[:8] & ~1) | length_bits
    stego_obj[8:16] = (stego_obj[8:16] & ~1) | seed_bits

    # LSB change order
    order = np.arange(start=2 * 8, stop=(2 + len(message)) * 8)
    if random:
        np.random.seed(seed)
        np.random.shuffle(order)

    # set each LSB to message bit
    stego_obj[order] = (stego_obj[order] & ~1) | message_bits

    stego_obj = stego_obj.reshape(original_shape)
    return stego_obj


def extract_message(obj: np.ndarray) -> str:
    obj = obj.flatten()

    # pack LSB to array
    lsb_array = np.array([bit & 1 for bit in obj])

    # get message length
    message_length = np.packbits(lsb_array[:8])[0]

    # get seed
    seed = np.packbits(lsb_array[8:16])[0]

    # detect if random
    random = seed != 0

    # get order
    order = np.arange(start=2 * 8, stop=(2 + message_length) * 8)
    if random:
        np.random.seed(seed)
        np.random.shuffle(order)

    message_bits = lsb_array[order]
    message = np.packbits(message_bits.reshape((len(message_bits) // 8, 8)))

    return message


def get_capacity(obj: np.ndarray):
    object_size = obj.shape
    lsb_count = np.product(object_size)
    byte_count = lsb_count / 8
    return byte_count


def is_valid(obj: np.ndarray):
    capacity = get_capacity(obj)
    return capacity > 2


def get_message_capacity(obj: np.ndarray):
    capacity = get_capacity(obj)

    # subtracting by 2 since 2 first bytes are used for stego-meta
    capacity -= 2
    return capacity
