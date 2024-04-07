import pytest

from src.buffer import StreamBuffer


@pytest.fixture
def test_data() -> tuple[str, str]:
    original = "Mixed \r\n Lines \r File \n Should \n\n Be Handled 砼"
    expected = original.replace("\r\n", "\n").replace("\r", "\n")

    return original, expected


@pytest.fixture
def test_file(tmpdir, test_data):
    original, expected = test_data

    path = tmpdir.join("test.bin")
    path.write(original.encode("utf-8"), mode="wb")
    return path, expected


def test_buffer_from_str(test_data):
    original, expected = test_data
    stream = StreamBuffer.from_str(original)

    output = ""
    while not stream.eof:
        output += stream.read_next_char()

    assert output == expected


def test_buffer_from_text_io(test_file):
    path, expected = test_file

    with open(path, "r", encoding="utf-8") as file:
        stream = StreamBuffer.from_text_io(file)

        output = ""
        while not stream.eof:
            output += stream.read_next_char()

        assert output == expected


def test_buffer_from_text_io_invalid_type():
    with pytest.raises(TypeError):
        StreamBuffer.from_text_io(object())


def test_buffer_from_binary_io(test_file):
    path, expected = test_file

    with open(path, "rb") as file:
        stream = StreamBuffer.from_binary_io(file)

        output = ""
        while not stream.eof:
            output += stream.read_next_char()

        assert output == expected


def test_counting_lines():
    stream = StreamBuffer.from_str("A\n\nB\nC")

    while (char := stream.read_next_char()) and char != "C":
        pass

    assert stream.line == 4
    assert stream.column == 1


def test_counting_newlines():
    stream = StreamBuffer.from_str("A\n")

    stream.read_next_char()
    stream.read_next_char()

    assert stream.line == 1
    assert stream.column == 2


def test_counting_columns():
    stream = StreamBuffer.from_str("A\n\nBEC")

    while (char := stream.read_next_char()) and char != "C":
        pass

    assert stream.line == 3
    assert stream.column == 3
    assert stream.position.line == 3
    assert stream.position.column == 3


def test_replacing_newlines():
    stream = StreamBuffer.from_str("H\rE\r\nL\nL\n\nO")

    output = ""
    while not stream.eof:
        output += stream.read_next_char()

    assert output == "H\nE\nL\nL\n\nO"


def test_handling_eof():
    stream = StreamBuffer.from_str("A")

    stream.read_next_char()

    assert stream.read_next_char() == ""
    assert stream.eof


def test_remember_last_char(test_data):
    original, expected = test_data
    stream = StreamBuffer.from_str(original)

    for _ in range(5):
        stream.read_next_char()

    char = stream.read_next_char()
    assert char == stream.char


def test_non_readable_stream(test_file):
    path, expected = test_file

    with open(path, "w", encoding="utf-8") as file:
        stream = StreamBuffer.from_text_io(file)

        with pytest.raises(RuntimeError):
            stream.read_next_char()


def test_iter(test_data):
    original, expected = test_data
    stream = StreamBuffer.from_str(original)

    output = ""
    for char in stream:
        output += char

    assert output == expected


def test_str(test_data):
    original, expected = test_data
    stream = StreamBuffer.from_str(original)

    for _ in range(5):
        stream.read_next_char()

    assert str(stream) == ("StreamBuffer"
                           "(position=Position(line=1, column=5), eof=False)")
