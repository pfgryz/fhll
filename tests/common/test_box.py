from src.common.box import Box


def test_box__full_box():
    box = Box[int](3)

    assert box


def test_box__empty_box():
    box = Box()

    assert not box


def test_box__put():
    box: Box[int] = Box()

    assert not box
    box.put(3)
    assert box


def test_box__value():
    box: Box[int] = Box(3)

    assert box.value() == 3


def test_box__take():
    box: Box[int] = Box(3)

    assert box
    assert box.take() == 3
    assert not box


def test_box__clear():
    box: Box[int] = Box(3)

    assert box
    box.clear()
    assert not box


def test_box__mutually_exclusive_take():
    box: Box[int] = Box(3)
    other: Box[str] = Box("other")

    box.add_mutually_exclusive(other)

    assert box
    assert other
    box.take()
    assert not box
    assert not other


def test_box__mutually_exclusive_clear():
    box: Box[int] = Box(3)
    other: Box[str] = Box("other")

    box.add_mutually_exclusive(other)

    assert box
    assert other
    box.clear()
    assert not box
    assert other
