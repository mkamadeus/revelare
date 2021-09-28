from revelare.utils import load_img
from revelare.steganography import extract_message, inject_message
import pytest
import numpy as np


@pytest.mark.parametrize(
    "message",
    [
        np.array(list("pisang"), dtype="|S1").view(np.uint8),
        np.array(list("pisang123"), dtype="|S1").view(np.uint8),
        np.array(list("!@#$%^&*()"), dtype="|S1").view(np.uint8),
        np.array(list("\xAA\xBB\xCC\xDD\xEE\xFF")).view(np.uint8),
    ],
)
def test_inject_extract_image(message):
    # load mock image
    b = load_img("./mocks/bmp/snail.bmp")

    # inject and extract message
    message = np.array(message.view(np.uint8))
    img = inject_message(b, message)
    extracted_message = extract_message(img)

    assert np.testing.assert_array_equal(extracted_message, message) is None


@pytest.mark.parametrize(
    "message,seed",
    [
        (np.array(list("pisang"), dtype="|S1").view(np.uint8), 42),
        (np.array(list("pisang123"), dtype="|S1").view(np.uint8), 69),
        (np.array(list("!@#$%^&*()"), dtype="|S1").view(np.uint8), 72),
        (np.array(list("\xAA\xBB\xCC\xDD\xEE\xFF")).view(np.uint8), 128),
    ],
)
def test_inject_extract_image_random(message, seed):
    # load mock image
    b = load_img("./mocks/bmp/snail.bmp")

    # inject and extract message
    message = np.array(message.view(np.uint8))
    img = inject_message(b, message, random=True, seed=seed)
    extracted_message = extract_message(img)

    assert np.testing.assert_array_equal(extracted_message, message) is None
