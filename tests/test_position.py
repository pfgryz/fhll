import pytest

from src.position import Position


def test_position():
    position = Position(1, 1)

    assert position.line == 1
    assert position.column == 1


def test_position_invalid_type():
    with pytest.raises(TypeError):
        Position(1.0, 1)


def test_position_invalid_column_number():
    with pytest.raises(ValueError):
        position = Position(2, 0)
