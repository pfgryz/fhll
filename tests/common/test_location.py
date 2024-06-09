import pytest

from src.common.location import Location
from src.common.position import Position


def test_location():
    location = Location(
        Position(1, 1),
        Position(3, 5)
    )

    assert location.begin.line == 1
    assert location.begin.column == 1
    assert location.end.column == 5


def test_location_invalid_begin_position_type():
    with pytest.raises(TypeError):
        Location(3, Position(1, 5))


def test_location_invalid_end_position_type():
    with pytest.raises(TypeError):
        Location(Position(1, 1), 3)


def test_location_invalid_begin_position_greater_line():
    with pytest.raises(ValueError):
        Location(
            Position(3, 1),
            Position(2, 4)
        )


def test_location_invalid_begin_position():
    with pytest.raises(ValueError):
        Location(
            Position(3, 10),
            Position(3, 4)
        )


def test_location_from_position():
    location = Location.at(Position(1, 1))

    assert location.begin == Position(1, 1)
    assert location.end == Position(1, 1)


def test_location_str():
    location = Location(Position(1, 1), Position(2, 3))

    assert str(location) == "1:1 - 2:3"


def test_location_lt():
    location_1 = Location(Position(1, 2), Position(2, 3))
    location_2 = Location(Position(1, 1), Position(3, 2))
    location_3 = Location(Position(3, 1), Position(3, 1))

    assert location_1 < location_3
    assert not (location_1 < location_2)
    assert not (location_2 < location_3)


def test_location_le():
    location_1 = Location(Position(1, 1), Position(2, 3))
    location_2 = Location(Position(1, 1), Position(2, 3))
    location_3 = Location(Position(3, 1), Position(4, 5))

    assert location_1 <= location_2
    assert location_1 <= location_3
