from copy import deepcopy
from typing import Optional, Callable

from multimethod import multimethod

from src.common.position import Position
from src.interface.ivisitor import IVisitor
from src.interpreter.box import Box
from src.interpreter.functions.ifunction_implementation import \
    IFunctionImplementation
from src.interpreter.operations.operation_registry import OperationRegistry
from src.interpreter.operations.operations_registry import OperationsRegistry
from src.interpreter.operations.operations_registry_old import \
    OperationsRegistryOld
from src.interpreter.stack.frame import Frame
from src.interpreter.errors import UndefinedFunctionError
from src.interpreter.functions.functions_registry import FunctionsRegistry
from src.interpreter.stack.value import Value
from src.interpreter.stack.variable import Variable
from src.interpreter.types.builtin_types import BuiltinTypes
from src.interpreter.types.typename import TypeName
from src.interpreter.types.types_registry import TypesRegistry
from src.interpreter.visitors.functions_collector import FunctionsCollector
from src.interpreter.visitors.name_visitor import NameVisitor
from src.interpreter.visitors.semantic.fn_call_validator import FnCallValidator
from src.interpreter.visitors.semantic.new_struct_validator import \
    NewStructValidator
from src.interpreter.visitors.semantic.return_validator import ReturnValidator
from src.interpreter.visitors.types_collector import TypesCollector
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.constant import Constant
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation import BoolOperation
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare import Compare
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.unary_operation import UnaryOperation
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType
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

    def __init__(self):
        # region Stack & State
        self._frame = Frame[str, Variable]()
        self._value: Box[Value]() = Box[Value]()

        self._return_break: Box[bool]() = Box[bool]()

        self._matcher_value: Optional[Value] = None
        self._matcher_break: Box[bool]() = Box[bool]()
        self._matcher_default: TypeName = TypeName("_")
        # endregion

        # region Visitors
        # Collectors
        self._types_collector = TypesCollector()
        self._functions_collector = FunctionsCollector(
            self._types_collector.types_registry
        )

        # Operations # @TODO: Should be collector
        self._operations_registry_old = OperationsRegistryOld()

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

        # region New Operations

        self._operations_registry = OperationsRegistry()

        self._operations_registry.register_binary(
            EBinaryOperationType.Add,
            BuiltinTypes.I32,
            BuiltinTypes.I32,
            lambda x, y: Value(type_name=x.type_name, value=x.value + y.value)
        )

        self._operations_registry.register_unary(
            EUnaryOperationType.Minus,
            BuiltinTypes.I32,
            lambda x: Value(type_name=x.type_name, value=-x.value)
        )

        self._operations_registry.register_cast(
            BuiltinTypes.I32,
            BuiltinTypes.BOOL,
            lambda x: Value(type_name=BuiltinTypes.BOOL, value=bool(x.value))
        )
        self._operations_registry.register_cast(
            BuiltinTypes.F32,
            BuiltinTypes.I32,
            lambda x: Value(type_name=BuiltinTypes.I32, value=int(x.value))
        )

        # endregion

        # region Temp Operations
        # Fill with basic operations @TODO: Move it somewhere

        def mul_int_int(x: Value, y: Value) -> Value:
            return Value(
                type_name=x.type_name,
                value=x.value * y.value
            )

        self._operations_registry_old.bool_operations.register_operation(
            EBoolOperationType.And,
            TypeName("*"),
            TypeName("&"),
            lambda x, y: Value(type_name=TypeName("bool"),
                               value=bool(x.value) and bool(y.value))
        )
        self._operations_registry_old.compare.register_operation(
            ECompareType.Equal,
            TypeName("*"),
            TypeName("&"),
            lambda x, y: Value(type_name=TypeName("bool"),
                               value=x.value == y.value)
        )
        self._operations_registry_old.compare.register_operation(
            ECompareType.Less,
            TypeName("*"),
            TypeName("&"),
            lambda x, y: Value(type_name=TypeName("bool"),
                               value=x.value < y.value)
        )

        self._operations_registry_old.binary_operations.register_operation(
            EBinaryOperationType.Add,
            TypeName("i32"),
            TypeName("i32"),
            lambda x, y: Value(type_name=x.type_name, value=x.value + y.value)
        )
        self._operations_registry_old.binary_operations.register_operation(
            EBinaryOperationType.Multiply,
            TypeName("i32"),
            TypeName("i32"),
            lambda x, y: mul_int_int(x, y)
        )
        self._operations_registry_old.unary_operations.register_operation(
            EUnaryOperationType.Minus,
            TypeName("i32"),
            None,
            lambda x: Value(type_name=x.type_name, value=-x.value)
        )
        self._operations_registry_old.cast.register_operation(
            "as",
            TypeName("i32"),
            TypeName("i32"),
            lambda x: x
        )

        # @TODO: Make it unviersal
        # @TODO: This can be used to all, should include relation between enums also
        self._operations_registry_old.is_compare.register_operation(
            "is",
            TypeName("*"),
            TypeName("*"),
            lambda x, y: Value(type_name=TypeName("bool"),
                               value=x.type_name == y)
        )
        # endregion

    # endregion

    # region Properties:

    @property
    def types_registry(self) -> TypesRegistry:
        return self._types_collector.types_registry

    @property
    def functions_registry(self) -> FunctionsRegistry:
        return self._functions_collector.functions_registry

    @property
    def operations_registry(self) -> OperationsRegistryOld:
        return self._operations_registry_old

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

    def run(self, name: str, *args: Value) -> Optional[Value]:
        if not (main := self.functions_registry.get_function(name)):
            raise UndefinedFunctionError(name, Position(1, 1))
        print('RUN')

        self._call_function(main, *args)

        return self._value.take()

    # endregion

    # region Helpers

    def _call_function(
            self,
            impl: IFunctionImplementation,
            *args: Value
    ):
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

    # endregion

    # region Statements

    @multimethod
    def visit(self, block: Block):
        self.create_frame()

        for statement in block.body:
            self.visit(statement)
            if self._return_break.value():
                break

        print('DROP')
        for v in self._frame.items():
            print(v)

        self.drop_frame()

    @multimethod
    def visit(self, variable_declaration: VariableDeclaration) -> None:
        # Get name
        self._name_visitor.visit(variable_declaration.name)
        name = self._name_visitor.name.take()

        # Get mutable state
        mutable = variable_declaration.mutable

        # Get type
        if variable_declaration.declared_type:
            self._name_visitor.visit(variable_declaration.declared_type)
            declared_type = self._name_visitor.type.take()

        # Get value
        if variable_declaration.value:
            self.visit(variable_declaration.value)
            value = deepcopy(self._value.take())
        else:
            value = self.types_registry.get_type(declared_type).instantiate()

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
        self.visit(assignment.access)
        memory = self._value.take()

        # Get value
        self.visit(assignment.value)
        value = deepcopy(self._value.take())

        memory.value = value.value

    @multimethod
    def visit(self, new_struct: NewStruct) -> None:
        self._name_visitor.visit(new_struct.variant)
        type_name = self._name_visitor.type.take()

        struct_impl = self.types_registry.get_struct(type_name)
        fields = {}

        for assignment in new_struct.assignments:
            self._name_visitor.visit(assignment.access)
            name = self._name_visitor.name.take()

            self.visit(assignment.value)
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
            self.visit(return_statement.value)

        self._return_break.put(True)

    @multimethod
    def visit(self, if_statement: IfStatement) -> None:
        self.visit(if_statement.condition)
        value = self._value.take()

        if self._operations_registry.cast(value, BuiltinTypes.BOOL).value:
            self.visit(if_statement.block)
            return

        if if_statement.else_block:
            self.visit(if_statement.else_block)

    @multimethod
    def visit(self, while_statement: WhileStatement) -> None:
        condition = True

        while condition:
            self.visit(while_statement.condition)
            condition = self._value.take()

            if not self._operations_registry.cast(
                    condition,
                    BuiltinTypes.BOOL
            ).value:
                break

            self.visit(while_statement.block)

            if self._return_break.value():
                break

    @multimethod
    def visit(self, match_statement: MatchStatement) -> None:
        self.visit(match_statement.expression)
        self._matcher_value = self._value.take()

        for matcher in match_statement.matchers:
            self.visit(matcher)

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
            self.visit(matcher.block)
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
            self.visit(argument)
            arguments.append(self._value.take())

        self._call_function(function_implementation, *arguments)

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
        self.visit(expression.left)
        left = self._value.take()
        self.visit(expression.right)
        right = self._value.take()

        self._value.put(
            operation(expression.op, left, right)
        )

    @multimethod
    def visit(self, expression: UnaryOperation) -> None:
        self.visit(expression.operand)
        operand = self._value.take()

        self._value.put(
            self._operations_registry.unary(expression.op, operand)
        )

    @multimethod
    def visit(self, expression: Cast) -> None:
        self.visit(expression.value)
        value = self._value.take()

        self._name_visitor.visit(expression.to_type)
        to_type = self._name_visitor.type.take()

        operation = self._operations_registry_old.cast.get_operation(
            "as",
            value.type_name,
            to_type
        )

        self._value.put(
            operation(value)
        )

    @multimethod
    def visit(self, expression: IsCompare) -> None:
        self.visit(expression.value)
        value = self._value.take()

        self._name_visitor.visit(expression.is_type)
        is_type = self._name_visitor.type.take()

        operation = self._operations_registry_old.is_compare.get_operation(
            "is",
            value.type_name,
            is_type
        )

        self._value.put(
            operation(value, is_type)
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
        self.visit(access.parent)
        self.visit(access.name)

    # endregion
