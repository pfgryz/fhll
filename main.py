from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print

from src.interpreter.interpreter import Interpreter
from src.lexer.errors import LexerError
from src.lexer.lexer import Lexer
from src.parser.ast.module import Module
from src.parser.errors import ParserError
from src.parser.parser import Parser
from src.tools.formatter import Formatter
from src.tools.printer import Printer
from src.utils.buffer import StreamBuffer

app = typer.Typer(no_args_is_help=True)

InputFile = Annotated[
    Path,
    typer.Option(
        "--in",
        "-i",
        exists=True,
        file_okay=True,
        readable=True
    )
]

OutputFile = Annotated[
    Optional[Path],
    typer.Option(
        "--out",
        "-o",
        exists=False
    )
]

Console = Annotated[
    Optional[bool],
    typer.Option(
        "--console",
        "-std",
        is_flag=True
    )
]


def warn(message: str) -> None:
    print("[bold yellow]Warn:[/bold yellow]", message)


def error(message: str) -> None:
    print("[bold red]Error:[/bold red]", message)


def parse_program(filepath: Path) -> Module:
    with open(filepath, "r") as handle:
        buffer = StreamBuffer.from_text_io(handle)
        lexer = Lexer(buffer)
        parser = Parser(lexer)

        try:
            program = parser.parse()
        except LexerError as ex:
            error(str(ex))
            raise typer.Exit(code=1)
        except ParserError as ex:
            error(str(ex))
            raise typer.Exit(code=1)

    return program


@app.command(
    name="print",
    help="Print the parser document object for given file"
)
def command_print(
        input_file: InputFile,
        output_file: OutputFile = None,
        console: Console = False
):
    program = parse_program(input_file)

    try:
        printer = Printer()
        printer.visit(program)
        content = printer.collect()
    except Exception as ex:
        error(f"Unknown exception {ex}")
        raise typer.Exit(code=2)

    if console:
        print(content)

    if output_file is not None:
        try:
            with open(output_file, "w") as handle:
                handle.write(content)
        except Exception as ex:
            error(str(ex))
            raise typer.Exit(code=3)

    if not console and output_file is None:
        error("No output specified")
        raise typer.Exit(code=1)


@app.command(
    name="fmt",
    help="Format the given input file"
)
def command_fmt(
        input_file: InputFile,
        output_file: OutputFile = None,
        console: Console = False,
        tab_size: Annotated[
            int,
            typer.Option(
                "--tab-size",
                "-t",
                min=1,
                max=32
            )
        ] = 4,
        use_tab: Annotated[
            bool,
            typer.Option(
                "--use-tab",
                is_flag=True
            )
        ] = False
):
    program = parse_program(input_file)

    try:
        formatter = Formatter(use_tab=use_tab, tab_size=tab_size)
        formatter.visit(program)
        content = formatter.collect()
    except Exception as ex:
        error(f"Unknown exception {ex}")
        raise typer.Exit(code=2)

    if console:
        print(content)

    if output_file is not None:
        try:
            with open(output_file, "w") as handle:
                handle.write(content)
        except Exception as ex:
            error(str(ex))
            raise typer.Exit(code=3)

    if not console and output_file is None:
        error("No output specified")
        raise typer.Exit(code=1)


@app.command(
    name="execute",
    help="Execute the given file"
)
def command_execute(
        input_file: InputFile,
        entry_point: str = "main"
):
    std_module = parse_program(Path("std/io.fhll"))
    program = parse_program(input_file)

    try:
        interpreter = Interpreter()
        interpreter.visit(std_module)
        interpreter.visit(program)
        result = interpreter.run(entry_point)

        if result is not None:
            print(f"Program exited with code {result.value}")
    except Exception as ex:
        error(f"Unknown exception {ex}")
        raise typer.Exit(code=2)


if __name__ == "__main__":
    app()
