import numpy as np


def inject_message(
    image: np.ndarray, message: str, random=False, random_seed=42
) -> np.ndarray:
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

    # set each LSB to message bit
    for i, bit in enumerate(info_bits):
        stego_image[i] = (stego_image[i] & ~1) | bit

    stego_image = stego_image.reshape(original_shape)
    return stego_image


def extract_message(image: np.ndarray, random=False, random_seed=42) -> np.ndarray:
    if len(image.shape) != 3:
        raise ValueError("unsupported image format")

    image = image.flatten()

    lsb_array = np.array([bit & 1 for bit in image])

    lsb_array = lsb_array.reshape((len(lsb_array) // 8, 8))

    message_length = np.packbits(lsb_array[0])[0]
    print(message_length)
    message = np.packbits(lsb_array[1 : message_length + 1]).tostring().decode("utf-8")
    print(message)

    # image = image.reshape(original_shape)
    # return image
