from multimethod import multimethod

from src.interface.ivisitor import IVisitor
from src.common.box import Box
from src.interpreter.errors import MissingReturnStatementError, \
    MissingReturnValueError, ReturnValueInVoidFunctionError
from src.interpreter.types.typename import TypeName
from src.interpreter.visitors.name_visitor import NameVisitor
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.module import Module
from src.parser.ast.node import Node
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.if_statement import IfStatement
from src.parser.ast.statements.match_statement import MatchStatement
from src.parser.ast.statements.matcher import Matcher
from src.parser.ast.statements.return_statement import ReturnStatement


class ReturnValidator(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self):
        self._name_visitor = NameVisitor()

        self._name: Box[str] = Box[str]()
        self._should_return_value: bool = False

        self._return: Box[bool] = Box[bool]()
        self._default: Box[bool] = Box[bool]()

    # endregion

    # region Visits

    @multimethod
    def visit(self, module: Module) -> None:
        for function_declaration in module.function_declarations:
            self._should_return_value = \
                function_declaration.return_type is not None

            self._name_visitor.visit(function_declaration.name)
            self._name.put(self._name_visitor.name.take())
            self.visit(function_declaration)

            if not self._return.take() and \
                    function_declaration.return_type is not None:
                raise MissingReturnStatementError(
                    self._name.take(),
                    function_declaration.location.begin
                )

    @multimethod
    def visit(self, function_declaration: FunctionDeclaration) -> None:
        self.visit(function_declaration.block)

    # endregion

    # region Visits - Statements

    @multimethod
    def visit(self, block: Block) -> None:
        for statement in block.body:
            self.visit(statement)
            if self._return.take():
                self._return.put(True)
                break
                # @HINT: Possible optimisation: Unreachable code

    @multimethod
    def visit(self, return_statement: ReturnStatement) -> None:
        if self._should_return_value and return_statement.value is None:
            raise MissingReturnValueError(
                self._name.value(),
                return_statement.location.begin
            )

        if not self._should_return_value and return_statement.value is not None:
            raise ReturnValueInVoidFunctionError(
                self._name.value(),
                return_statement.location.begin
            )

        self._return.put(True)

    @multimethod
    def visit(self, if_statement: IfStatement) -> None:
        self.visit(if_statement.block)
        block_return = self._return.take()
        else_return = False

        if if_statement.else_block is not None:
            self.visit(if_statement.else_block)
            else_return = self._return.take()

        self._return.put(block_return and else_return)

    @multimethod
    def visit(self, match_statement: MatchStatement) -> None:
        returning = True
        has_default = False

        for matcher in match_statement.matchers:
            self.visit(matcher)
            returning = returning and self._return.take()
            has_default = has_default or self._default.take()

        self._return.put(returning and has_default)

    @multimethod
    def visit(self, matcher: Matcher) -> None:
        self._name_visitor.visit(matcher.checked_type)

        checked_type = self._name_visitor.type.take()
        self._default.put(
            checked_type and checked_type == TypeName.parse("_")
        )

        self.visit(matcher.block)

    @multimethod
    def visit(self, node: Node) -> None:
        ...

    # endregion
