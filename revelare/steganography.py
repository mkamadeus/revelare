import numpy as np


def inject_message(image: np.ndarray, message: np.ndarray, random=False, seed=42) -> np.ndarray:
    if len(image.shape) != 3:
        raise ValueError("unsupported image format")

    original_shape = object.shape
    stego_object = object.flatten()

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
    stego_object[:8] = (stego_object[:8] & ~1) | length_bits
    stego_object[8:16] = (stego_object[8:16] & ~1) | seed_bits

    # LSB change order
    order = np.arange(start=2 * 8, stop=(2 + len(message)) * 8)
    if random:
        np.random.seed(seed)
        np.random.shuffle(order)

    # set each LSB to message bit
    stego_object[order] = (stego_object[order] & ~1) | message_bits

    stego_object = stego_object.reshape(original_shape)
    return stego_object


def extract_message(object: np.ndarray) -> str:
    if len(object.shape) != 3:
        raise ValueError("unsupported object format")

    object = object.flatten()

    # pack LSB to array
    lsb_array = np.array([bit & 1 for bit in object])

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


def get_capacity(object: np.ndarray):
    object_size = object.shape
    lsb_count = np.product(object_size)
    byte_count = lsb_count / 8
    return byte_count


def is_valid(object: np.ndarray):
    capacity = get_capacity(object)
    return capacity > 2


def get_message_capacity(object: np.ndarray):
    capacity = get_capacity(object)

    # subtracting by 2 since 2 first bytes are used for stego-meta
    capacity -= 2
    return capacity
