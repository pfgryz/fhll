from multimethod import multimethod

from src.common.position import Position
from src.interface.ivisitor import IVisitor
from src.interpreter.box import Box
from src.interpreter.stack.frame import Frame
from src.interpreter.errors import UndefinedFunctionError
from src.interpreter.functions.functions_registry import FunctionsRegistry
from src.interpreter.stack.value import Value
from src.interpreter.stack.variable import Variable
from src.interpreter.types.types_registry import TypesRegistry
from src.interpreter.visitors.functions_collector import FunctionsCollector
from src.interpreter.visitors.name_visitor import NameVisitor
from src.interpreter.visitors.semantic.fn_call_validator import FnCallValidator
from src.interpreter.visitors.semantic.new_struct_validator import \
    NewStructValidator
from src.interpreter.visitors.semantic.return_validator import ReturnValidator
from src.interpreter.visitors.types_collector import TypesCollector
from src.parser.ast.constant import Constant
from src.parser.ast.module import Module
from src.parser.ast.node import Node
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.variable_declaration import VariableDeclaration


class Interpreter(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self):
        # Stack
        self._frame = Frame[str, Variable]()
        self._value: Box[Value]() = Box[Value]()

        # Collectors
        self._types_collector = TypesCollector()
        self._functions_collector = FunctionsCollector(
            self._types_collector.types_registry
        )

        # Validators
        self._fn_call_validator = FnCallValidator(
            self._functions_collector.functions_registry
        )
        self._new_struct_validator = NewStructValidator(
            self._types_collector.types_registry
        )
        self._return_validator = ReturnValidator()

        # Other
        self._name_visitor = NameVisitor()

    # endregion

    # region Properties

    @property
    def types_registry(self) -> TypesRegistry:
        return self._types_collector.types_registry

    @property
    def functions_registry(self) -> FunctionsRegistry:
        return self._functions_collector.functions_registry

    # endregion

    # region Frames Management

    def create_frame(self):
        self._frame = Frame(self._frame)

    def drop_frame(self):
        self._frame = self._frame.parent

    # endregion

    # region Module

    @multimethod
    def visit(self, module: Module) -> None:
        self._types_collector.visit(module)
        self._functions_collector.visit(module)
        self._fn_call_validator.visit(module)
        self._new_struct_validator.visit(module)
        self._return_validator.visit(module)

    def run(self, name: str):
        if not (main := self.functions_registry.get_function(name)):
            raise UndefinedFunctionError(name, Position(1, 1))
        print('RUN')
        # Create context
        main.call(self)

    # endregion

    # region Statements

    @multimethod
    def visit(self, block: Block):
        self.create_frame()
        print('Hi, i block')

        for statement in block.body:
            self.visit(statement)

        self.drop_frame()

    @multimethod
    def visit(self, variable_declaration: VariableDeclaration) -> None:
        # Get name
        self._name_visitor.visit(variable_declaration.name)
        name = self._name_visitor.name.take()

        # Get mutable state
        mutable = variable_declaration.mutable

        # Get type
        self._name_visitor.visit(variable_declaration.declared_type)
        declared_type = self._name_visitor.type.take()

        # Get value
        self.visit(variable_declaration.value)
        value = self._value.take()

        self._frame.set(name, Variable(
            mutable=mutable,
            value=value
        ))
        ...

    # endregion

    # region Expressions

    @multimethod
    def visit(self, constant: Constant) -> None:
        ...

    # endregion
