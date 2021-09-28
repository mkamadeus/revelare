import numpy as np
import pytest
from revelare.steganography import get_capacity, get_message_capacity, inject_message

sample_image = np.array(
    [
        [[255, 255, 255], [255, 255, 255], [255, 255, 255]],
        [[255, 255, 255], [255, 255, 255], [255, 255, 255]],
        [[255, 255, 255], [255, 255, 255], [255, 255, 255]],
        [[255, 255, 255], [255, 255, 255], [255, 255, 255]],
        [[255, 255, 255], [255, 255, 255], [255, 255, 255]],
        [[255, 255, 255], [255, 255, 255], [255, 255, 255]],
    ]
)
sample_message = np.array([], dtype=np.uint8)
sample_target = np.array(
    [
        [[254, 254, 254], [254, 254, 254], [254, 254, 254]],
        [[254, 254, 254], [254, 254, 254], [254, 254, 254]],
        [[254, 254, 254], [254, 254, 254], [254, 254, 254]],
        [[254, 254, 254], [254, 254, 254], [254, 254, 254]],
        [[254, 254, 254], [254, 255, 255], [255, 255, 255]],
        [[255, 255, 255], [255, 255, 255], [255, 255, 255]],
    ]
)


def test_inject_message():
    result = inject_message(sample_image, sample_message)
    assert np.testing.assert_array_equal(result, sample_target) is None


@pytest.mark.parametrize(
    "shape,capacity",
    [
        ((512, 512, 3), 98304),
        ((256, 256, 3), 24576),
        ((12, 12, 3), 54),
        ((5, 5, 3), 9),
    ],
)
def test_get_capacity(shape, capacity):
    obj = np.zeros(shape)
    assert get_capacity(obj) == capacity


@pytest.mark.parametrize(
    "shape,capacity",
    [
        ((512, 512, 3), 98299),
        ((256, 256, 3), 24571),
        ((12, 12, 3), 49),
        ((5, 5, 3), 4),
    ],
)
def test_get_message_capacity(shape, capacity):
    obj = np.zeros(shape)
    assert get_message_capacity(obj) == capacity
