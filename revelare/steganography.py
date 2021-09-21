import numpy as np
from icecream import ic


def inject_message(image: np.ndarray, message: str, random=False, seed=42) -> np.ndarray:
    if len(image.shape) != 3:
        raise ValueError("unsupported image format")

    original_shape = image.shape
    stego_image = image.flatten()

    # get bits from message
    message_bits = np.unpackbits(np.array(list(map(ord, message)), dtype=np.uint8))

    # get bits from message length
    length_bits = np.unpackbits(np.array([len(message)], dtype=np.uint8))

    # append info together
    info_bits = np.concatenate((length_bits, message_bits))

    # LSB change order
    order = np.arange((len(message) + 1) * 8)
    ic(order)
    if random:
        np.random.seed(seed)
        order = np.random.shuffle(order)

    # set each LSB to message bit
    for i, bit in list(zip(order, info_bits)):
        ic(stego_image[i], bit)
        stego_image[i] = (stego_image[i] & ~1) | bit
        ic(stego_image[i])

    stego_image = stego_image.reshape(original_shape)
    return stego_image


def extract_message(image: np.ndarray, random=False, seed=42) -> str:
    if len(image.shape) != 3:
        raise ValueError("unsupported image format")

    image = image.flatten()

    lsb_array = np.array([bit & 1 for bit in image])

    lsb_array = lsb_array.reshape((len(lsb_array) // 8, 8))

    # LSB change order
    order = np.arange(len(lsb_array))
    ic(order)
    if random:
        np.random.seed(seed)
        order = np.random.shuffle(order)

    message_length = np.packbits(lsb_array[order[0]])[0]
    message = np.packbits(lsb_array[order[1 : message_length + 1]]).tobytes().decode("utf-8")

    return message
