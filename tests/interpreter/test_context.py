import pytest

from src.interpreter.context import Context


# region Single Context

def test_context__len():
    context = Context(store={'a': 3})

    assert len(context) == 1


def test_context__contains():
    context = Context(store={'a': 3})

    assert "a" in context


def test_context__getitem():
    context = Context(store={'a': 3})

    assert context["a"] == 3


def test_context__getitem_key_error():
    context = Context(store={'a': 3})

    with pytest.raises(KeyError):
        _ = context["b"]


def test_context__setitem():
    context = Context(store={'a': 3})

    context["b"] = 4

    assert context["b"] == 4


def test_context__keys():
    context = Context(store={'a': 3})

    assert context.keys() == ["a"]


def test_context__values():
    context = Context(store={'a': 3})

    assert context.values() == [3]


def test_context__items():
    context = Context(store={'a': 3})

    assert context.items() == [("a", 3)]


def test_context__get():
    context = Context(store={'a': 3})

    assert context.get("a") == 3
    assert context.get("b") is None


def test_context__set():
    context = Context(store={'a': 3})

    context.set("c", 5)

    assert context["c"] == 5


# endregion

# region Chained Context

def test_context__chained__len():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert len(context) == 3


def test_context__chained__contains():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert "a" in context
    assert "b" in context
    assert "c" in context
    assert "c" not in parent


def test_context__chained__getitem():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context["a"] == 3
    assert context["c"] == 6


def test_context__chained__setitem():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    context["a"] = 10
    context["c"] = 20

    assert context["a"] == 10
    assert context["c"] == 20
    assert parent["a"] == 10


def test_context__chained__keys():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context.keys() == ["c", "a", "b"]


def test_context__chained__keys_no_chain():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context.keys(chain=False) == ["c"]


def test_context__chained__values():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context.values() == [6, 3, 4]


def test_context__chained__values_no_chain():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context.values(chain=False) == [6]


def test_context__chained__items():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context.items() == [("c", 6), ("a", 3), ("b", 4)]


def test_context__chained__items_no_chain():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context.items(chain=False) == [("c", 6)]


def test_context__chained__get():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context.get("a") == 3


def test_context__chained__get_no_chain():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context.get("a", chain=False) is None
    assert context.get("b", chain=False) is None
    assert context.get("c", chain=False) is not None


def test_context__chained__set():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    context.set("d", 10)

    assert context.get("d") == 10
    assert context.get("d", chain=False) == 10


def test_context__chained__set_chain():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    context.set("b", 10)
    print(context._store)
    assert context.get("b") == 10
    assert context.get("b", chain=False) is None


def test_context__chained__set_no_chain():
    parent = Context(store={'a': 3, 'b': 4})
    context = Context(parent, store={'c': 6})

    assert context.get("b", chain=False) is None

    context.set("b", 10, chain=False)

    assert context.get("b") == 10
    assert context.get("b", chain=False) == 10

# endregion