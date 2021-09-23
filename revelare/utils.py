from PIL import Image
from scipy.io import wavfile
import numpy as np


def load_img(path):
    img = Image.open(path)
    img = img.convert("RGB")
    img_bytes = np.asarray(img)
    return img_bytes


def write_img(image_bytes, path):
    image = Image.fromarray(image_bytes)
    image.save(path)


def load_wav(path):
    audio = wavfile.read(path)
    return audio


def write_wav(audio_bytes, sample_rate, path):
    wavfile.write(path, sample_rate, audio_bytes)
