from PIL import Image
import numpy as np


def bmp_to_bytes(path):
    img = Image.open(path)
    img = img.convert("RGB")
    img_bytes = np.asarray(img)
    return img_bytes


def bytes_to_bmp(image_bytes, path):
    image = Image.fromarray(image_bytes)
    image.save(path)
