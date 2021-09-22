import numpy as np


def rms(image_1: np.ndarray, image_2: np.ndarray):
    if image_1.shape != image_2.shape:
        raise ValueError("image shape is different")

    return (((image_1 - image_2) ** 2) / (image_1.shape[0] * image_1.shape[1])) ** 0.5


def psnr(image_1: np.ndarray, image_2: np.ndarray):
    return 20 * np.log(255 / rms(image_1, image_2), 10)
