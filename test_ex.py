import pytest
from ex import ex_funcs, ex_funcs2


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (3, 2, 1),
        (2, 3, 5),
        (10, 20, 30),
    ],
)
def test_ex_funcs(x: int, y: int, expected: int) -> None:
    """ex_funcsが期待通りに動作するかをテストする。
    Test point:
        -xとyの和がexpectedと等しいかどうかを確認する。
    Args:
        x (int): The first input value.
        y (int): The second input value.
        expected (int): The expected result of ex_funcs(x, y).
    """
    assert ex_funcs(x, y) == expected


'''
@pytest.mark.parametrize(
    "x, y, expected",
    [
        (3, 2, 1),
        (10, 5, 5),
        (11, 1, 10),
        (100, 1, 99),
    ],
)
def test_ex_funcs2(
    x: int, 
    y: int, 
    expected: int) -> None:
    """ex_funcs2が期待通りに動作するかをテストする。
    Test point:
        xとyの差がexpectedと等しいかどうかを確認する。

    Args:
        x (int): The first input value.
        y (int): The second input value.
        expected (int): The expected result of ex_funcs2(x, y).
    """
    assert ex_funcs2(x, y) == expected

'''
