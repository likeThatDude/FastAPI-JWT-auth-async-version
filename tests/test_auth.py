import pytest
from contextlib import nullcontext as not_rais

from services.for_test import Calculator


def test_first():
    assert 1 == 1


def test_second():
    assert 2 == 2


@pytest.fixture
def print_any():
    print('Тест пройден')


@pytest.fixture(scope='session')
def setup_db():
    Base.metadata.drop_all()
    Base.metadata.create_all()


@pytest.mark.usefixtures('print_any')
class TestCalculator:
    @staticmethod
    @pytest.mark.parametrize(
        'x,y,res, expectation',
        [
            (4, 2, 2, not_rais()),
            (6, 3, 2, not_rais()),
            (7, 2, 3.5, not_rais()),
            (7, "2", 3.5, pytest.raises(TypeError)),
            (2, 0, 6, pytest.raises(ZeroDivisionError))
        ]
    )
    def test_calculator_divide(x, y, res, expectation):
        with expectation:
            assert Calculator.divide(x, y) == res

    @staticmethod
    @pytest.mark.parametrize(
        'x,y,res, expectation',
        [
            (4, 2, 6, not_rais()),
            (6, 3, 9, not_rais()),
            (7, 2, 9, not_rais()),
            (7, "2", 3.5, pytest.raises(TypeError))
        ]
    )
    def test_add(x, y, res, expectation):
        with expectation:
            assert Calculator.add(x, y) == res
