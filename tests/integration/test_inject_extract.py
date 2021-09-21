from revelare.utils import load_bmp
from revelare.steganography import extract_message, inject_message
import pytest


@pytest.mark.parametrize("message", ["pisang", "pisang123", "!@#$%^&*()"])
def test_inject_extract(message):
    # load mock image
    b = load_bmp("./mocks/bmp/snail.bmp")

    # inject and extract message
    img = inject_message(b, message)
    extracted_message = extract_message(img)

    assert extracted_message == message
