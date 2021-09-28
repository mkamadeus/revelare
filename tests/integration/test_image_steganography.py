from revelare.utils import load_img
from revelare.steganography import extract_message, inject_message
import pytest
import numpy as np


@pytest.mark.parametrize(
    "message",
    [
        np.array(list("pisang")).view(np.uint8),
        np.array(list("pisang123")).view(np.uint8),
        np.array(list("!@#$%^&*()")).view(np.uint8),
        np.array(list("\xAA\xBB\xCC\xDD\xEE\xFF")).view(np.uint8),
        np.array(
            list(
                "asttokens==2.0.5attrs==21.2.0bitstring==3.1.9black==21.9b0click==8.0.1colorama==0.4.4executing==0.8.1flake8==3.9.2icecream==2.1.1iniconfig==1.1.1mccabe==0.6.1mypy-extensions==0.4.3numpy==1.21.2packaging==21.0pathspec==0.9.0Pillow==8.3.2platformdirs==2.3.0pluggy==1.0.0py==1.10.0pycodestyle==2.7.0pyflakes==2.3.1Pygments==2.10.0pyparsing==2.4.7pyqt5==5.15.4pytest==6.2.5regex==2021.8.28scipy==1.7.1six==1.16.0toml==0.10.2tomli==1.2.1typing-extensions==3.10.0.2"
            )
        ).view(np.uint8),
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
        (np.array(list("pisang")).view(np.uint8), 42),
        (np.array(list("pisang123")).view(np.uint8), 69),
        (np.array(list("!@#$%^&*()")).view(np.uint8), 72),
        (np.array(list("\xAA\xBB\xCC\xDD\xEE\xFF")).view(np.uint8), 128),
        (
            np.array(
                list(
                    "asttokens==2.0.5attrs==21.2.0bitstring==3.1.9black==21.9b0click==8.0.1colorama==0.4.4executing==0.8.1flake8==3.9.2icecream==2.1.1iniconfig==1.1.1mccabe==0.6.1mypy-extensions==0.4.3numpy==1.21.2packaging==21.0pathspec==0.9.0Pillow==8.3.2platformdirs==2.3.0pluggy==1.0.0py==1.10.0pycodestyle==2.7.0pyflakes==2.3.1Pygments==2.10.0pyparsing==2.4.7pyqt5==5.15.4pytest==6.2.5regex==2021.8.28scipy==1.7.1six==1.16.0toml==0.10.2tomli==1.2.1typing-extensions==3.10.0.2"
                ),
                dtype="|S1",
            ).view(np.uint8),
            128,
        ),
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
