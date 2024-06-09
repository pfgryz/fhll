import pytest

from src.common.position import Position


def test_position():
    position = Position(1, 1)

    assert position.line == 1
    assert position.column == 1


def test_position_invalid_line_type():
    with pytest.raises(TypeError):
        Position(1.0, 1)


def test_position_invalid_column_type():
    with pytest.raises(TypeError):
        Position(1, 1.0)


def test_position_invalid_line_number():
    with pytest.raises(ValueError):
        Position(0, 1)


def test_position_invalid_column_number():
    with pytest.raises(ValueError):
        Position(2, 0)


def test_position_lt__compare_to_non_position():
    position = Position(1, 1)

    assert not position < 3


def test_position_lt__higher_line():
    position_1 = Position(1, 2)
    position_2 = Position(2, 1)

    assert position_1 < position_2


def test_position_lt__same_line_higher_column():
    position_1 = Position(3, 2)
    position_2 = Position(3, 5)

    assert position_1 < position_2


def test_position_lt__same_position():
    position_1 = Position(1, 1)

    assert not position_1 < position_1


def test_position_le__less():
    position_1 = Position(3, 2)
    position_2 = Position(4, 5)

    assert position_1 < position_2


def test_position_le__equal():
    position = Position(3, 2)

    assert position <= position
