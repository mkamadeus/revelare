import pytest
from revelare.utils import load_img, load_wav


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


@pytest.mark.parametrize(
    "path,sampling,shape",
    [
        ("./mocks/wav/lounge.wav", 22050, (5646848, 2)),
        ("./mocks/wav/sample.wav", 8000, (268237, 2)),
    ],
)
def test_load_wav(path, sampling, shape):
    sample_rate, wav = load_wav(path)
    assert sampling == sample_rate
    assert wav.shape == shape
