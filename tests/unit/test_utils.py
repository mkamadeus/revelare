import pytest
from revelare.utils import load_img


@pytest.mark.parametrize(
    "path,shape",
    [
        ("./mocks/bmp/lena.bmp", (512, 512, 3)),
        ("./mocks/bmp/snail.bmp", (256, 256, 3)),
        ("./mocks/png/lena.png", (512, 512, 3)),
        ("./mocks/png/blackbuck.png", (512, 512, 3)),
    ],
)
def test_load_img(path, shape):
    image = load_img(path)
    assert image.shape == shape
