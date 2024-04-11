import pytest
from contextlib import nullcontext as not_rais


@pytest.fixture
def divide_set():
    return ['x,y,res, expectation',
            [
                (4, 2, 2, not_rais()),
                (6, 3, 2, not_rais()),
                (7, 2, 3.5, not_rais()),
                (7, "2", 3.5, pytest.raises(TypeError)),
                (2, 0, 6, pytest.raises(ZeroDivisionError))
            ]
            ]
