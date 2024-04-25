from src.utils.builder import StringBuilder


def test_builder_creation():
    builder = StringBuilder()
    assert builder.length == 0
    assert builder.build() == ""


def test_builder_initial_value():
    builder = StringBuilder("ini")

    assert builder.length == 3
    assert builder.build() == "ini"


def test_builder_add_value():
    builder = StringBuilder()

    for char in ["a", "b", "c"]:
        builder += char

    assert builder.length == 3
    assert builder.build() == "abc"


def test_builder_build():
    builder = StringBuilder()

    for char in "Hello\\nWorld":
        builder += char

    assert builder.length == 12
    assert builder.build() == "Hello\\nWorld"
