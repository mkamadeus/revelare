import numpy as np


def inject_message(
    image: np.ndarray, message: np.ndarray, random=False, seed=42
) -> np.ndarray:
    if len(image.shape) != 3:
        raise ValueError("unsupported image format")

    original_shape = image.shape
    stego_image = image.flatten()

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
    stego_image[:8] = (stego_image[:8] & ~1) | length_bits
    stego_image[8:16] = (stego_image[8:16] & ~1) | seed_bits

    # LSB change order
    order = np.arange(start=2 * 8, stop=(2 + len(message)) * 8)
    if random:
        np.random.seed(seed)
        np.random.shuffle(order)

    # set each LSB to message bit
    stego_image[order] = (stego_image[order] & ~1) | message_bits

    stego_image = stego_image.reshape(original_shape)
    return stego_image


def extract_message(image: np.ndarray) -> str:
    if len(image.shape) != 3:
        raise ValueError("unsupported image format")

    image = image.flatten()

    # pack LSB to array
    lsb_array = np.array([bit & 1 for bit in image])

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
