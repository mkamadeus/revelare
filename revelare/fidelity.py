import numpy as np


def rmse(image_1: np.ndarray, image_2: np.ndarray):
    if image_1.shape != image_2.shape:
        raise ValueError("image shape is different")

    return np.sqrt(np.mean((image_1 - image_2) ** 2))


def psnr(image_1: np.ndarray, image_2: np.ndarray):
    return 20 * np.log(255 / rmse(image_1, image_2), 10)
