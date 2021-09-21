import pytest
from revelare.utils import load_bmp


@pytest.mark.parametrize(
    "path,shape", [("./mocks/bmp/lena.bmp", (512, 512, 3)), ("./mocks/bmp/snail.bmp", (256, 256, 3))]
)
def test_load_bmp(path, shape):
    image = load_bmp(path)
    assert image.shape == shape
