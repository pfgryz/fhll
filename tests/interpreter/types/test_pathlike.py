import pytest

from src.interpreter.types.pathlike import PathLike


def test_pathlike__eq():
    pathlike = PathLike("i32")

    assert pathlike == PathLike("i32")


def test_pathlike__hash():
    pathlike = PathLike("i32")
    mapping = {pathlike: 3}
    assert mapping[PathLike("i32")] == 3


def test_pathlike__repr():
    pathlike = PathLike("i32")
    assert repr(pathlike) == "PathLike('i32')"


def test_pathlike__str():
    pathlike = PathLike("Main", "Ui")
    assert str(pathlike) == "Main/Ui"


def test_pathlike__path():
    pathlike = PathLike("Main", "Ui")
    assert pathlike.path == ("Main", "Ui")


def test_pathlike__extend():
    pathlike = PathLike("Main", "Ui")
    pathlike_child = pathlike.extend("Btn")

    assert pathlike_child.path == ("Main", "Ui", "Btn")


def test_pathlike__parse():
    pathlike = PathLike.parse("Main/Ui")
    assert pathlike.path == ("Main", "Ui")


def test_pathlike__following_digit():
    with pytest.raises(ValueError):
        PathLike.parse("3Main/Ui")


def test_pathlike__invalid_character():
    with pytest.raises(ValueError):
        PathLike.parse("Main./Ui")
