from multimethod import multimethod

from src.interface.ivisitor import IVisitor
from src.interpreter.errors import UnknownTypeError, \
    UndefinedStructError
from src.interpreter.types.typename import TypeName
from src.interpreter.types.types_registry import TypesRegistry
from src.interpreter.visitors.name_visitor import NameVisitor
from src.parser.ast.cast import Cast
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
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


class StaticTypeValidator(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self, types_registry: TypesRegistry):
        self._name_visitor = NameVisitor()
        self._types_registry = types_registry

    # endregion

    # region Visits

    @multimethod
    def visit(self, module: Module) -> None:
        for function_declaration in module.function_declarations:
            self.visit(function_declaration)

    @multimethod
    def visit(self, function_declaration: FunctionDeclaration) -> None:
        self.visit(function_declaration.block)

    # endregion

    # region Visits - Statements
    @multimethod
    def visit(self, block: Block) -> None:
        for statement in block.body:
            self.visit(statement)

    @multimethod
    def visit(self, assignment: Assignment) -> None:
        self.visit(assignment.value)

    @multimethod
    def visit(self, fn_call: FnCall) -> None:
        for argument in fn_call.arguments:
            self.visit(argument)

    @multimethod
    def visit(self, return_statement: ReturnStatement) -> None:
        if return_statement.value is not None:
            self.visit(return_statement.value)

    @multimethod
    def visit(self, if_statement: IfStatement) -> None:
        self.visit(if_statement.condition)
        self.visit(if_statement.block)

        if if_statement.else_block is not None:
            self.visit(if_statement.else_block)

    @multimethod
    def visit(self, while_statement: WhileStatement) -> None:
        self.visit(while_statement.condition)
        self.visit(while_statement.block)

    @multimethod
    def visit(self, match_statement: MatchStatement) -> None:
        self.visit(match_statement.expression)
        for matcher in match_statement.matchers:
            self.visit(matcher)

    # endregion

    # region Visits - Expression

    @multimethod
    def visit(self, expression: BoolOperation) -> None:
        self.visit(expression.left)
        self.visit(expression.right)

    @multimethod
    def visit(self, expression: Compare) -> None:
        self.visit(expression.left)
        self.visit(expression.right)

    @multimethod
    def visit(self, expression: BinaryOperation) -> None:
        self.visit(expression.left)
        self.visit(expression.right)

    @multimethod
    def visit(self, expression: UnaryOperation) -> None:
        self.visit(expression.operand)

    @multimethod
    def visit(self, node: Node) -> None:
        ...

    # endregion

    # region Visits - Checks

    def check(self, node: Name | VariantAccess, struct: bool = False):
        self._name_visitor.visit(node)
        type_name = self._name_visitor.type.take()

        if not self._types_registry.get_type(type_name) \
                or (struct and not self._types_registry.get_struct(type_name)):
            raise UnknownTypeError(type_name, node.location.begin)

    @multimethod
    def visit(self, variable_declaration: VariableDeclaration) -> None:
        if variable_declaration.declared_type:
            self.check(variable_declaration.declared_type)

        if variable_declaration.value is not None:
            self.visit(variable_declaration.value)

    @multimethod
    def visit(self, new_struct: NewStruct) -> None:
        self.check(new_struct.variant)

        for assignment in new_struct.assignments:
            self.visit(assignment)

    @multimethod
    def visit(self, matcher: Matcher) -> None:
        self._name_visitor.visit(matcher.checked_type)
        type_name = self._name_visitor.type.take()

        if type_name != TypeName("_"):
            self.check(matcher.checked_type)

        self.visit(matcher.block)

    @multimethod
    def visit(self, cast: Cast) -> None:
        self.check(cast.to_type)

        self.visit(cast.value)

    @multimethod
    def visit(self, is_compare: IsCompare) -> None:
        self.check(is_compare.is_type)

        self.visit(is_compare.value)

    # endregion
