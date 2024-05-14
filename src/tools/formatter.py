from enum import Enum
from io import StringIO

from multimethod import multimethod

from src.interface.ivisitor import IVisitor, IVisitable
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.constant import Constant
from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.declaration.parameter import Parameter
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.bool_operation import BoolOperation
from src.parser.ast.expressions.compare import Compare
from src.parser.ast.expressions.unary_operation import UnaryOperation
from src.parser.ast.is_compare import IsCompare
from src.parser.ast.module import Module
from src.parser.ast.name import Name
from src.parser.ast.node import Node
from src.parser.ast.statements.assignment import Assignment
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.fn_call import FnCall
from src.parser.ast.statements.if_statement import IfStatement
from src.parser.ast.statements.match_statement import MatchStatement
from src.parser.ast.statements.matcher import Matcher
from src.parser.ast.statements.new_struct_statement import NewStruct
from src.parser.ast.statements.return_statement import ReturnStatement
from src.parser.ast.statements.variable_declaration import VariableDeclaration
from src.parser.ast.statements.while_statement import WhileStatement
from src.parser.ast.variant_access import VariantAccess


class EIndent(Enum):
    Space = " "
    Tab = "\t"


class Formatter(IVisitor):

    # region Dunder Methods

    def __init__(self, tab_size: int = 4, use_tab: bool = False):
        self._indent = 0
        self._tab_size = tab_size
        self._use_tab = use_tab
        self._semicolon = False
        self._buffer = StringIO()

    # endregion

    # region Indentation

    def down(self) -> None:
        self._indent += 1

    def up(self) -> None:
        if self._indent > 0:
            self._indent -= 1

    def emit(self) -> None:
        if self._indent < 1:
            return

        if self._use_tab:
            self.write("\t" * self._indent, eol=False)
        else:
            self.write(" " * self._tab_size * self._indent, eol=False)

    def emit_semicolon(self) -> None:
        if not self._semicolon:
            return

        self._semicolon = False
        self.write(";")

    # endregion

    # region Printing

    def write(self, message: str, eol: bool = False) -> None:
        self._buffer.write(message)

        if eol:
            self._buffer.write("\n")

    def collect(self, clear: bool = False) -> str:
        value = self._buffer.getvalue()

        if clear:
            self.reset()

        return value

    def reset(self) -> None:
        self._indent = -1
        self._buffer = StringIO()

    # endregion

    # region Visitor

    def visit(self, node: IVisitable) -> None:
        return self._visit(node)

    @multimethod
    def _visit(self, node: Node) -> None:
        print(node)
        raise NotImplementedError()

    # endregion

    # region Module

    @multimethod
    def _visit(self, module: Module):
        elements = [] + module.function_declarations \
                   + module.struct_declarations \
                   + module.enum_declarations
        elements.sort(key=lambda x: x.location)

        for idx, element in enumerate(elements):
            self.visit(element)

            if idx < len(elements) - 1:
                self.write("\n\n")

            self.write("\n")

    # endregion

    # region Functions

    @multimethod
    def _visit(self, function_declaration: FunctionDeclaration) -> None:
        self.write("fn ")
        self.visit(function_declaration.name)
        self.write("(")

        for idx, parameter in enumerate(function_declaration.parameters):
            self.visit(parameter)

            if idx != len(function_declaration.parameters) - 1:
                self.write(",")

        self.write(") ")
        self.visit(function_declaration.block)

    @multimethod
    def _visit(self, parameter: Parameter) -> None:
        if parameter.mutable:
            self.write("mut ")

        self.visit(parameter.name)
        self.write(": ")
        self.visit(parameter.type)

    # endregion

    # region Struct

    @multimethod
    def _visit(self, struct_declaration: StructDeclaration) -> None:
        self.emit()
        self.write("struct ")
        self.visit(struct_declaration.name)

        self.write(" {", eol=True)
        self.down()

        for field in struct_declaration.fields:
            self.emit()
            self.visit(field)
            self.write(";", eol=True)

        self.up()
        self.emit()
        self.write("}")

    @multimethod
    def _visit(self, field_declaration: FieldDeclaration) -> None:
        self.visit(field_declaration.name)
        self.write(": ")
        self.visit(field_declaration.type)

    # endregion

    # region Enum

    @multimethod
    def _visit(self, enum_declaration: EnumDeclaration) -> None:
        self.emit()
        self.write("enum ")
        self.visit(enum_declaration.name)

        self.write(" {", eol=True)
        self.down()

        for idx, variant in enumerate(enum_declaration.variants):
            self.visit(variant)
            self.write(";", eol=True)

            if idx < len(enum_declaration.variants) - 1:
                self.write("\n")

        self.up()
        self.emit()
        self.write("}")

    # endregion

    # region Statements

    @multimethod
    def _visit(self, block: Block) -> None:
        self.write("{", eol=True)
        self.down()

        for statement in block.body:
            self.emit()
            self.visit(statement)

            self.emit_semicolon()
            self.write("", eol=True)

        self.up()
        self.emit()
        self.write("}")

    @multimethod
    def _visit(self, declaration: VariableDeclaration) -> None:
        if declaration.mutable:
            self.write("mut ")

        self.write("let ")
        self.visit(declaration.name)

        if declaration.type:
            self.write(": ")
            self.visit(declaration.type)

        if declaration.value:
            self.write(" = ")
            self.visit(declaration.value)

        self._semicolon = True

    @multimethod
    def _visit(self, assignment: Assignment) -> None:
        self.visit(assignment.name)
        self.write(" = ")
        self.visit(assignment.value)

        self._semicolon = True

    @multimethod
    def _visit(self, fn_call: FnCall) -> None:
        self.visit(fn_call.name)
        self.write("(")

        for idx, argument in enumerate(fn_call.arguments):
            self.visit(argument)

            if idx != len(fn_call.arguments) - 1:
                self.write(", ")

        self.write(")")

        self._semicolon = True

    @multimethod
    def _visit(self, return_statement: ReturnStatement) -> None:
        self.write("return")

        if return_statement.value:
            self.write(" ")
            self.visit(return_statement.value)

        self._semicolon = True

    @multimethod
    def _visit(self, if_statement: IfStatement) -> None:
        self.write("if (")
        self.visit(if_statement.condition)
        self.write(") ")
        self.visit(if_statement.block)

        if if_statement.else_block:
            self.write("else ")
            self.visit(if_statement.else_block)

    @multimethod
    def _visit(self, while_statement: WhileStatement) -> None:
        self.write("while (")
        self.visit(while_statement.condition)
        self.write(") ")
        self.visit(while_statement.block)

    @multimethod
    def _visit(self, match_statement: MatchStatement) -> None:
        self.write("match (")
        self.visit(match_statement.expression)

        self.write(" ) {", eol=True)
        self.down()

        for matcher in match_statement.matchers:
            self.emit()
            self.visit(matcher)
            self.write(";", eol=True)

        self.up()
        self.emit()
        self.write("}")

    @multimethod
    def _visit(self, matcher: Matcher) -> None:
        self.visit(matcher.type)
        self.write(" ")
        self.visit(matcher.name)
        self.write(" => ")
        self.visit(matcher.block)

    # endregion

    # region Access

    @multimethod
    def _visit(self, name: Name) -> None:
        self.write(name.identifier)

    @multimethod
    def _visit(self, access: Access) -> None:
        self.visit(access.parent)
        self.write(".")
        self.visit(access.name)

    @multimethod
    def _visit(self, variant_access: VariantAccess) -> None:
        self.visit(variant_access.parent)
        self.write("::")
        self.visit(variant_access.name)

    # endregion

    # region Expressions

    @multimethod
    def _visit(self, new_struct: NewStruct) -> None:
        self.visit(new_struct.variant)

        self.write("{")

        for assignment in new_struct.assignments:
            self.write(" ")
            self.visit(assignment)
            self.write(";")

        self.write(" }")

    @multimethod
    def _visit(self, constant: Constant) -> None:
        self.write(str(constant.value))

    @multimethod
    def _visit(self, is_compare: IsCompare) -> None:
        self.visit(is_compare.value)
        self.write(" is ")
        self.visit(is_compare.type)

    @multimethod
    def _visit(self, cast: Cast) -> None:
        self.visit(cast.value)
        self.write(" as ")
        self.visit(cast.type)

    @multimethod
    def _visit(self, unary_operation: UnaryOperation) -> None:
        self.write(unary_operation.op.to_operator())
        self.visit(unary_operation.operand)

    @multimethod
    def _visit(self, binary_operation: BinaryOperation) -> None:
        self.visit(binary_operation.left)
        self.write(f" {binary_operation.op.to_operator()} ")
        self.visit(binary_operation.right)

    @multimethod
    def _visit(self, compare: Compare) -> None:
        self.visit(compare.left)
        self.write(f" {compare.mode.to_operator()} ")
        self.visit(compare.right)

    @multimethod
    def _visit(self, bool_operation: BoolOperation) -> None:
        self.visit(bool_operation.left)
        self.write(f" {bool_operation.op.to_operator()} ")
        self.visit(bool_operation.right)

    # endregion
