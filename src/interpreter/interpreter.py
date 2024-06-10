from collections import deque
from copy import deepcopy
from typing import Optional, Callable

from multimethod import multimethod

from src.common.position import Position
from src.flags import Flags
from src.interface.ivisitor import IVisitor
from src.common.box import Box
from src.interpreter.functions.builtin_functions_registry import \
    BuiltinFunctionsRegistry
from src.interpreter.functions.ifunction_implementation import \
    IFunctionImplementation
from src.interpreter.operations.builtin_operations_registry import \
    BuiltinOperationsRegistry
from src.interpreter.operations.operations_registry import OperationsRegistry
from src.interpreter.stack.frame import Frame
from src.interpreter.errors import UndefinedFunctionError, PanicBreak, \
    PanicError, MaximumRecursionError
from src.interpreter.functions.functions_registry import FunctionsRegistry
from src.interpreter.stack.value import Value
from src.interpreter.stack.variable import Variable
from src.interpreter.types.builtin_types import BuiltinTypes
from src.interpreter.types.typename import TypeName
from src.interpreter.types.types_registry import TypesRegistry
from src.interpreter.visitors.functions_collector import FunctionsCollector
from src.interpreter.visitors.name_visitor import NameVisitor
from src.interpreter.visitors.semantic.dynamic_type_validator import \
    DynamicTypeValidator
from src.interpreter.visitors.semantic.fn_call_validator import FnCallValidator
from src.interpreter.visitors.semantic.new_struct_validator import \
    NewStructValidator
from src.interpreter.visitors.semantic.return_validator import ReturnValidator
from src.interpreter.visitors.semantic.static_type_validator import \
    StaticTypeValidator
from src.interpreter.visitors.types_collector import TypesCollector
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.constant import Constant
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
from src.parser.interface.itree_like_expression import ITreeLikeExpression


class Interpreter(IVisitor[Node]):

    # region Dunder Methods

    def __init__(self, flags: Flags = None):
        self._flags = flags if flags is not None else Flags()

        # region Stack & State
        self._stack = deque()
        self._frame = Frame[str, Variable]()
        self._value: Box[Value]() = Box[Value]()

        self._recursion: int = 0
        self._return_break: Box[bool]() = Box[bool]()

        self._matcher_value: Optional[Value] = None
        self._matcher_break: Box[bool]() = Box[bool]()
        self._matcher_default: TypeName = TypeName("_")
        # endregion

        # region Visitors
        # Collectors
        self._types_collector = TypesCollector()
        self._functions_collector = FunctionsCollector(
            self._types_collector.types_registry,
            BuiltinFunctionsRegistry()
        )

        # @TODO: It should be moved to collector (allow custom impls)
        self._operations_registry = BuiltinOperationsRegistry()

        # Validators
        self._fn_call_validator = FnCallValidator(
            self._functions_collector.functions_registry
        )
        self._new_struct_validator = NewStructValidator(
            self._types_collector.types_registry
        )
        self._return_validator = ReturnValidator()
        self._static_type_validator = StaticTypeValidator(
            self._types_collector.types_registry
        )
        self._dynamic_type_validator = DynamicTypeValidator(
            self._types_collector.types_registry,
            self._functions_collector.functions_registry,
            self._operations_registry
        )

        # Other
        self._name_visitor = NameVisitor()

        # endregion

    # endregion

    # region Properties:

    @property
    def value(self) -> Box[Value]:
        return self._value

    @property
    def frame(self) -> Frame:
        return self._frame

    @property
    def types_registry(self) -> TypesRegistry:
        return self._types_collector.types_registry

    @property
    def functions_registry(self) -> FunctionsRegistry:
        return self._functions_collector.functions_registry

    @property
    def operations_registry(self) -> OperationsRegistry:
        return self._operations_registry

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
        self._static_type_validator.visit(module)
        self._dynamic_type_validator.visit(module)

    def run(self, name: str, *args: Value) -> Optional[Value]:
        if not (main := self.functions_registry.get_function(name)):
            raise UndefinedFunctionError(name, Position(1, 1))

        try:
            self._call_function(main, *args)
        except PanicBreak as panic_break:
            position = Position(1, 1) \
                if len(self._stack) == 0 else self._stack[0].location.begin

            raise PanicError(
                panic_break.panic_message,
                position=position
            )

        return self._value.take()

    # endregion

    # region Helpers

    def _call_function(
            self,
            impl: IFunctionImplementation,
            *args: Value
    ):
        self._recursion += 1
        if self._recursion > self._flags.maximum_recursion:
            raise MaximumRecursionError()

        # Create frame with arguments
        self.create_frame()
        for arg, (name, (mutable, _)) in zip(args, impl.parameters.items()):
            self._frame.set(
                name,
                Variable(
                    mutable=mutable,
                    value=deepcopy(arg)
                )
            )

        # Call function
        impl.call(self)

        # Drop frame with arguments
        self.drop_frame()
        self._recursion -= 1

    def _register_visit(self, node: Node):
        self._stack.append(node)
        self.visit(node)
        self._stack.pop()

    # endregion

    # region Statements

    @multimethod
    def visit(self, block: Block):
        self.create_frame()

        for statement in block.body:
            self._register_visit(statement)
            if self._return_break.value():
                break

        self.drop_frame()

    @multimethod
    def visit(self, variable_declaration: VariableDeclaration) -> None:
        # Get name
        self._name_visitor.visit(variable_declaration.name)
        name = self._name_visitor.name.take()

        # Get mutable state
        mutable = variable_declaration.mutable

        # Get type
        declared_type = None
        if variable_declaration.declared_type:
            self._name_visitor.visit(variable_declaration.declared_type)
            declared_type = self._name_visitor.type.take()

        # Get value
        value = None
        if variable_declaration.value:
            self._register_visit(variable_declaration.value)
            value = deepcopy(self._value.take())
        else:
            value = self.types_registry.get_type(declared_type).instantiate()

        if declared_type and not declared_type.is_base_of(value.type_name):
            value = self.operations_registry.cast(value, declared_type)

        self._frame.set(
            name,
            Variable(
                mutable=mutable,
                value=value
            ),
            chain=False
        )

    @multimethod
    def visit(self, assignment: Assignment) -> None:
        # Get name
        self._register_visit(assignment.access)
        memory = self._value.take()

        # Get value
        self._register_visit(assignment.value)
        value = deepcopy(self._value.take())

        # Cast to proper type
        if not memory.type_name.is_base_of(value.type_name):
            value = self.operations_registry.cast(value, memory.type_name)

        memory.value = value.value

    @multimethod
    def visit(self, new_struct: NewStruct) -> None:
        self._name_visitor.visit(new_struct.variant)
        type_name = self._name_visitor.type.take()

        struct_impl = self.types_registry.get_struct(type_name)
        fields = {} # @TODO: Default values

        for assignment in new_struct.assignments:
            self._name_visitor.visit(assignment.access)
            name = self._name_visitor.name.take()

            self._register_visit(assignment.value)
            value = deepcopy(self._value.take())
            fields[name] = value

        self._value.put(
            Value(
                type_name=type_name,
                value=struct_impl.instantiate(fields)
            )
        )

    @multimethod
    def visit(self, return_statement: ReturnStatement) -> None:
        if return_statement.value is not None:
            self._register_visit(return_statement.value)

        self._return_break.put(True)

    @multimethod
    def visit(self, if_statement: IfStatement) -> None:
        self._register_visit(if_statement.condition)
        value = self._value.take()

        if self._operations_registry.cast(value, BuiltinTypes.BOOL).value:
            self._register_visit(if_statement.block)
            return

        if if_statement.else_block:
            self._register_visit(if_statement.else_block)

    @multimethod
    def visit(self, while_statement: WhileStatement) -> None:
        condition = True

        while condition:
            self._register_visit(while_statement.condition)
            condition = self._value.take()

            if not self._operations_registry.cast(
                    condition,
                    BuiltinTypes.BOOL
            ).value:
                break

            self._register_visit(while_statement.block)

            if self._return_break.value():
                break

    @multimethod
    def visit(self, match_statement: MatchStatement) -> None:
        self._register_visit(match_statement.expression)
        self._matcher_value = self._value.take()

        for matcher in match_statement.matchers:
            self._register_visit(matcher)

            if self._matcher_break.take():
                break

            if self._return_break.value():
                break

    @multimethod
    def visit(self, matcher: Matcher) -> None:
        self._name_visitor.visit(matcher.name)
        name = self._name_visitor.name.take()

        self._name_visitor.visit(matcher.checked_type)
        checked_type = self._name_visitor.type.take()

        value = self._matcher_value

        if self._operations_registry.is_type(value, checked_type).value \
                or checked_type == self._matcher_default:
            self.create_frame()
            self._frame.set(
                name,
                Variable(
                    mutable=False,
                    value=value
                ),
                chain=False
            )
            self._register_visit(matcher.block)
            self._matcher_break.put(True)
            self.drop_frame()

    @multimethod
    def visit(self, fn_call: FnCall) -> None:
        self._name_visitor.visit(fn_call.name)
        name = self._name_visitor.name.take()

        function_implementation = self.functions_registry.get_function(
            name
        )

        arguments = []
        for argument in fn_call.arguments:
            self._register_visit(argument)
            arguments.append(self._value.take())

        self._call_function(function_implementation, *arguments)
        self._return_break.put(False)

    # endregion

    # region Expressions

    @multimethod
    def visit(self, expression: BoolOperation) -> None:
        self._two_argument_operation(
            expression,
            self._operations_registry.bool
        )

    @multimethod
    def visit(self, expression: Compare) -> None:
        self._two_argument_operation(
            expression,
            self._operations_registry.compare
        )

    @multimethod
    def visit(self, expression: BinaryOperation) -> None:
        self._two_argument_operation(
            expression,
            self._operations_registry.binary
        )

    def _two_argument_operation(
            self,
            expression: ITreeLikeExpression | Compare,
            operation: Callable
    ):
        self._register_visit(expression.left)
        left = self._value.take()
        self._register_visit(expression.right)
        right = self._value.take()

        self._value.put(
            operation(expression.op, left, right)
        )

    @multimethod
    def visit(self, expression: UnaryOperation) -> None:
        self._register_visit(expression.operand)
        operand = self._value.take()

        self._value.put(
            self._operations_registry.unary(expression.op, operand)
        )

    @multimethod
    def visit(self, expression: Cast) -> None:
        self._register_visit(expression.value)
        value = self._value.take()

        self._name_visitor.visit(expression.to_type)
        to_type = self._name_visitor.type.take()

        self._value.put(
            self._operations_registry.cast(value, to_type)
        )

    @multimethod
    def visit(self, expression: IsCompare) -> None:
        self._register_visit(expression.value)
        value = self._value.take()

        self._name_visitor.visit(expression.is_type)
        is_type = self._name_visitor.type.take()

        self._value.put(
            self._operations_registry.is_type(value, is_type)
        )

    @multimethod
    def visit(self, constant: Constant) -> None:
        type_name = TypeName.parse(constant.type.to_name())
        self._value.put(
            Value(
                type_name=type_name,
                value=constant.value
            )
        )

    # endregion

    # region Names

    @multimethod
    def visit(self, name: Name) -> None:
        if self._value.value():
            self._value.put(
                self._value.take().value.get(name.identifier)
            )
        else:
            self._value.put(
                self._frame.get(name.identifier).value
            )

    @multimethod
    def visit(self, access: Access) -> None:
        self._register_visit(access.parent)
        self._register_visit(access.name)

    # endregion
