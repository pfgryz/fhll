from multimethod import multimethod

from src.common.shall import shall
from src.interface.ivisitor import IVisitor
from src.interpreter.errors import InternalError, UndefinedFunctionCallError, \
    TooFewArgumentsError, TooManyArgumentsError
from src.interpreter.functions.functions_registry import FunctionsRegistry
from src.interpreter.visitors.name_visitor import NameVisitor
from src.parser.ast.cast import Cast
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.bool_operation import BoolOperation
from src.parser.ast.expressions.compare import Compare
from src.parser.ast.expressions.unary_operation import UnaryOperation
from src.parser.ast.is_compare import IsCompare
from src.parser.ast.module import Module
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


class FnCallValidator(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self, functions_registry: FunctionsRegistry):
        self._name_visitor = NameVisitor()
        self._functions_registry = functions_registry

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
    def visit(self, variable_declaration: VariableDeclaration) -> None:
        if variable_declaration.value is not None:
            self.visit(variable_declaration.value)

    @multimethod
    def visit(self, assignment: Assignment) -> None:
        self.visit(assignment.value)

    @multimethod
    def visit(self, new_struct: NewStruct) -> None:
        for assignment in new_struct.assignments:
            self.visit(assignment)

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

    @multimethod
    def visit(self, matcher: Matcher) -> None:
        self.visit(matcher.block)

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
    def visit(self, expression: Cast) -> None:
        self.visit(expression.value)

    @multimethod
    def visit(self, expression: IsCompare) -> None:
        self.visit(expression.value)

    @multimethod
    def visit(self, node: Node) -> None:
        ...

    # endregion

    # region Visits - FnCall

    @multimethod
    def visit(self, fn_call: FnCall) -> None:
        self._name_visitor.visit(fn_call.name)
        name = shall(
            self._name_visitor.name.take(),
            InternalError,
            "Cannot get name for function call"
        )

        if not (function := self._functions_registry.get_function(name)):
            raise UndefinedFunctionCallError(name, fn_call.location.begin)

        if len(fn_call.arguments) < len(function.parameters):
            raise TooFewArgumentsError(name, fn_call.location.begin)

        if len(fn_call.arguments) > len(function.parameters):
            raise TooManyArgumentsError(name, fn_call.location.begin)

    # endregion
