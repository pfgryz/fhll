from io import StringIO

from multimethod import multimethod

from src.interface.ivisitor import IVisitor
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


class IndentManager:

    def __init__(self, printer: 'Printer'):
        self._printer = printer

    def __enter__(self):
        self._printer.down()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._printer.up()


class Printer(IVisitor):

    # region Dunder Methods

    def __init__(self):
        self._indent = -1
        self._buffer = StringIO()
        self._indent_manager = IndentManager(self)

    # endregion

    # region Indentation

    def down(self) -> None:
        self._indent += 1

    def up(self) -> None:
        if self._indent > -1:
            self._indent -= 1

    @property
    def indent(self) -> IndentManager:
        return self._indent_manager

    # endregion

    # region Printing

    def write(self, message: str, eol: bool = True,
              use_indent: bool = True) -> None:
        if use_indent and self._indent > 0:
            self._buffer.write("\t" * self._indent)

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

    def visit(self, node) -> None:
        print(node)
        with self.indent:
            return self._visit(node)

    @multimethod
    def _visit(self, node: Node) -> None:
        raise NotImplementedError()

    # endregion

    # region Module

    @multimethod
    def _visit(self, module: Module) -> None:
        self.write(
            f"Module:"
        )

        with self.indent:
            self.write(
                f"name: {module.name}"
            )
            self.write(
                f"path: {module.path}"
            )

            if len(module.function_declarations):
                self.write("functions:")
                for function_declaration in module.function_declarations:
                    self.visit(function_declaration)
            else:
                self.write("functions: []")

            if len(module.struct_declarations):
                self.write("structs:")
                for struct_declaration in module.struct_declarations:
                    self.visit(struct_declaration)
            else:
                self.write("structs: []")

            if len(module.enum_declarations):
                self.write("enums:")
                for enum_declaration in module.enum_declarations:
                    self.visit(enum_declaration)
            else:
                self.write("enums: []")

    # endregion

    # region Functions

    @multimethod
    def _visit(self, function_declaration: FunctionDeclaration) -> None:
        self.write(
            f"FunctionDeclaration ({function_declaration.location}):"
        )

        with self.indent:
            self.write("name:")
            self.visit(function_declaration.name)

            self.write("parameters:")
            for parameter in function_declaration.parameters:
                self.visit(parameter)

            if function_declaration.return_type:
                self.write("returns:")
                self.visit(function_declaration.return_type)
            else:
                self.write("returns: None")

            self.write("body:")
            self.visit(function_declaration.block)

    @multimethod
    def _visit(self, parameter: Parameter) -> None:
        self.write(
            f"Parameter ({parameter.location}):"
        )

        with self.indent:
            self.write(f"name:")
            self.visit(parameter.name)

            self.write(f"mutable: {parameter.mutable}")

            self.write("type:")
            self.visit(parameter.type)

    # endregion

    # region Struct

    @multimethod
    def _visit(self, struct_declaration: StructDeclaration) -> None:
        self.write(
            f"StructDeclaration ({struct_declaration.location}):"
        )

        with self.indent:
            self.write("name:")
            self.visit(struct_declaration.name)

            self.write("fields:")
            for field in struct_declaration.fields:
                self.visit(field)

    @multimethod
    def _visit(self, field_declaration: FieldDeclaration) -> None:
        self.write(
            f"FieldDeclaration ({field_declaration.location}):"
        )

        with self.indent:
            self.write("name:")
            self.visit(field_declaration.name)

            self.write("type:")
            self.visit(field_declaration.type)

    # endregion

    # region Enum

    @multimethod
    def _visit(self, enum_declaration: EnumDeclaration) -> None:
        self.write(
            f"EnumDeclaration ({enum_declaration.location}):"
        )

        with self.indent:
            self.write("name:")
            self.visit(enum_declaration.name)

            if len(enum_declaration.variants):
                self.write("variants:")
                for variant in enum_declaration.variants:
                    self.visit(variant)
            else:
                self.write("variants: []")

    # endregion

    # region Statements

    @multimethod
    def _visit(self, block: Block) -> None:
        if len(block.body) == 0:
            self.write("[]")
            return

        print(block.body)

        for statement in block.body:
            print("\t", statement)
            self.visit(statement)

    @multimethod
    def _visit(self, declaration: VariableDeclaration) -> None:
        self.write(
            f"Declaration ({declaration.location}):"
        )

        with self.indent:
            self.visit(declaration.name)

            self.write(
                f"mutable: {str(declaration.mutable)}"
            )

            if declaration.type:
                self.write("type:")
                self.visit(declaration.type)
            else:
                self.write("type: None")

            if declaration.value:
                self.write("value:")
                self.visit(declaration.value)
            else:
                self.write("value: None")

    @multimethod
    def _visit(self, assignment: Assignment) -> None:
        self.write(
            f"Assignment ({assignment.location}):"
        )

        with self.indent:
            self.visit(assignment.name)

            self.write("value:")
            self.visit(assignment.value)

    @multimethod
    def _visit(self, fn_call: FnCall) -> None:
        self.write(
            f"FnCall ({fn_call.location}):"
        )

        with self.indent:
            self.visit(fn_call.name)

            self.write("arguments:")
            for argument in fn_call.arguments:
                self.visit(argument)

    @multimethod
    def _visit(self, return_statement: ReturnStatement) -> None:
        if return_statement.value is not None:
            self.write(
                f"ReturnStatement ({return_statement.location}):"
            )
            self.visit(return_statement.value)
        else:
            self.write("ReturnStatement ({return_statement.location})")

    @multimethod
    def _visit(self, if_statement: IfStatement) -> None:
        self.write(
            f"IfStatement ({if_statement.location}):"
        )

        with self.indent:
            self.write("condition:")
            self.visit(if_statement.condition)

            self.write("block:")
            self.visit(if_statement.block)

            if if_statement.else_block is not None:
                self.write("else:")
                self.visit(if_statement.else_block)

    @multimethod
    def _visit(self, while_statement: WhileStatement) -> None:
        self.write(
            f"WhileStatement ({while_statement.location}):"
        )

        with self.indent:
            self.write("condition:")
            self.visit(while_statement.condition)

            self.write("block:")
            self.visit(while_statement.block)

    @multimethod
    def _visit(self, match_statement: MatchStatement) -> None:
        self.write(
            f"MatchStatement ({match_statement.location}):"
        )

        with self.indent:
            self.write("expression:")
            self.visit(match_statement.expression)

            self.write("matchers:")
            for matcher in match_statement.matchers:
                self.visit(matcher)

    @multimethod
    def _visit(self, matcher: Matcher) -> None:
        self.write(
            f"Matcher ({matcher.location}):"
        )

        with self.indent:
            self.write("type:")
            self.visit(matcher.type)

            self.write("name:")
            self.visit(matcher.name)

            self.write("block:")
            self.visit(matcher.block)

    # endregion

    # region Access

    @multimethod
    def _visit(self, name: Name) -> None:
        self.write(
            f"Name ({name.location}): {name.identifier}"
        )

    @multimethod
    def _visit(self, access: Access) -> None:
        self.write(
            f"Access ({access.location}):"
        )

        with self.indent:
            self.write("name:")
            self.visit(access.name)

            self.write("parent:")
            self.visit(access.parent)

    @multimethod
    def _visit(self, variant_access: VariantAccess) -> None:
        self.write(
            f"VariantAccess ({variant_access.location}):"
        )

        with self.indent:
            self.write("name:")
            self.visit(variant_access.name)

            self.write("parent:")
            self.visit(variant_access.parent)

    # endregion

    # region Expressions

    @multimethod
    def _visit(self, new_struct: NewStruct) -> None:
        self.write(
            f"NewStruct ({new_struct.location}):"
        )

        with self.indent:
            self.write("struct:")
            self.visit(new_struct.variant)

            self.write("assignments:")
            for assignment in new_struct.assignments:
                self.visit(assignment)

    @multimethod
    def _visit(self, constant: Constant) -> None:
        self.write(
            f"Constant ({constant.location}):"
        )

        with self.indent:
            self.write(
                f"value: {constant.value}"
            )

    @multimethod
    def _visit(self, is_compare: IsCompare) -> None:
        self.write(
            f"IsCompare ({is_compare.location}):"
        )

        with self.indent:
            self.write("value:")
            self.visit(is_compare.value)

            self.write("is:")
            self.visit(is_compare.type)

    @multimethod
    def _visit(self, cast: Cast) -> None:
        self.write(
            f"Cast ({cast.location}):"
        )

        with self.indent:
            self.write("value:")
            self.visit(cast.value)

            self.write("to:")
            self.visit(cast.type)

    @multimethod
    def _visit(self, unary_operation: UnaryOperation) -> None:
        self.write(
            f"UnaryOperation ({unary_operation.location}):"
        )

        with self.indent:
            self.write(
                f"op: {unary_operation.op.name}"
            )

            self.write("value:")
            self.visit(unary_operation.operand)

    @multimethod
    def _visit(self, binary_operation: BinaryOperation) -> None:
        self.write(
            f"BinaryOperation ({binary_operation.location}):"
        )

        with self.indent:
            self.write(
                f"op: {binary_operation.op.name}"
            )

            self.write("left:")
            self.visit(binary_operation.left)

            self.write("right:")
            self.visit(binary_operation.right)

    @multimethod
    def _visit(self, compare: Compare) -> None:
        self.write(
            f"Compare ({compare.location}):"
        )

        with self.indent:
            self.write(
                f"mode: {compare.mode.name}"
            )

            self.write("left:")
            self.visit(compare.left)

            self.write("right:")
            self.visit(compare.right)

    @multimethod
    def _visit(self, bool_operation: BoolOperation) -> None:
        self.write(
            "BooleanOperation ({bool_operation.location}):"
        )

        with self.indent:
            self.write(
                f"op: {bool_operation.op.name}"
            )

            self.write("left:")
            self.visit(bool_operation.left)

            self.write("right:")
            self.visit(bool_operation.right)

    # endregion
