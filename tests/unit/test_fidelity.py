from revelare.fidelity import rmse
import numpy as np
import pytest


@pytest.mark.parametrize(
    "target,output,error",
    [
        (np.array([[1, 1], [2, 3]]), np.array([[1, 1], [2, 3]]), 0),
        (np.array([1, 2, 3]), np.array([1, 2, 6]), 3 ** 0.5),
    ],
)
def test_rmse(target, output, error):
    assert target.shape == output.shape
    err = rmse(target, output)
    assert err == error
