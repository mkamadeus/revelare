from revelare.utils import load_wav
from revelare.steganography import extract_message, inject_message
import pytest
import numpy as np


@pytest.mark.parametrize(
    "path,message,seed",
    [
        ("./mocks/wav/sample.wav", np.array(list("pisang")).view(np.uint8), -1),
        ("./mocks/wav/sample.wav", np.array(list("pisang123")).view(np.uint8), -1),
        ("./mocks/wav/sample.wav", np.array(list("!@#$%^&*()")).view(np.uint8), -1),
        ("./mocks/wav/sample.wav", np.array(list("\xAA\xBB\xCC\xDD\xEE\xFF")).view(np.uint8), -1),
        (
            "./mocks/wav/sample.wav",
            np.array(list("abcdefghijklmnopqrstuvwxyz" * 50)).view(np.uint8),
            -1,
        ),
        ("./mocks/wav/sample.wav", np.array(list("pisang")).view(np.uint8), 42),
        ("./mocks/wav/sample.wav", np.array(list("pisang123")).view(np.uint8), 69),
        ("./mocks/wav/sample.wav", np.array(list("!@#$%^&*()")).view(np.uint8), 72),
        ("./mocks/wav/sample.wav", np.array(list("\xAA\xBB\xCC\xDD\xEE\xFF")).view(np.uint8), 128),
        (
            "./mocks/wav/sample.wav",
            np.array(list("abcdefghijklmnopqrstuvwxyz" * 50)).view(np.uint8),
            -1,
        ),
    ],
)
def test_inject_extract_image(path, message, seed):
    # load mock image
    _, b = load_wav("./mocks/wav/sample.wav")
    filename = path.split("/")[-1]

    # check randomness
    random = seed != -1

    # inject and extract message
    message = np.array(message.view(np.uint8))
    img = inject_message(b, message, filename, random=random, seed=seed)
    extracted_filename, extracted_message = extract_message(img)

    assert filename == extracted_filename
    assert np.testing.assert_array_equal(extracted_message, message) is None
