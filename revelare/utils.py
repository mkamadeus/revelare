from PIL import Image
import numpy as np


def load_bmp(path):
    img = Image.open(path)
    img = img.convert("RGB")
    img_bytes = np.asarray(img)
    return img_bytes


def write_bmp(image_bytes, path):
    image = Image.fromarray(image_bytes)
    image.save(path)
