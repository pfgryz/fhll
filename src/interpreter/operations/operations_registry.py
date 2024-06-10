from typing import Callable

from src.common.registrable import Registrable
from src.common.shall import shall
from src.interpreter.errors import MissingOperationImplementationError, \
    OperationImplementationAlreadyRegisteredError
from src.interpreter.stack.value import Value
from src.interpreter.types.builtin_types import BuiltinTypes
from src.interpreter.types.typename import TypeName
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType

type BoolImplementation = Callable[[Value, Value], Value]
type CompareImplementation = Callable[[Value, Value], Value]
type BinaryImplementation = Callable[[Value, Value], Value]
type UnaryImplementation = Callable[[Value], Value]
type CastImplementation = Callable[[Value], Value]

type TwoArgument[Op, Impl] = dict[Op, dict[TypeName, dict[TypeName, Impl]]]

type Bool = TwoArgument[EBoolOperationType, BoolImplementation]
type Compare = TwoArgument[ECompareType, CompareImplementation]
type Binary = TwoArgument[EBinaryOperationType, BinaryImplementation]
type Unary = dict[EUnaryOperationType, dict[TypeName, UnaryImplementation]]
type Cast = dict[TypeName, dict[TypeName, CastImplementation]]


def bool_impl(op: EBoolOperationType, first: TypeName, second: TypeName):
    def decorator(func):
        Registrable.register_func(
            func,
            lambda x: x.register_bool(op, first, second, func)
        )
        return func

    return decorator


def compare_impl(op: ECompareType, first: TypeName, second: TypeName):
    def decorator(func):
        Registrable.register_func(
            func,
            lambda x: x.register_compare(op, first, second, func)
        )
        return func

    return decorator


def binary_impl(op: EBinaryOperationType, first: TypeName, second: TypeName):
    def decorator(func):
        Registrable.register_func(
            func,
            lambda x: x.register_binary(op, first, second, func)
        )
        return func

    return decorator


def unary_impl(op: EUnaryOperationType, type_name: TypeName):
    def decorator(func):
        Registrable.register_func(
            func,
            lambda x: x.register_unary(op, type_name, func)
        )
        return func

    return decorator


def cast_impl(from_type: TypeName, to_type: TypeName):
    def decorator(func):
        Registrable.register_func(
            func,
            lambda x: x.register_cast(from_type, to_type, func)
        )
        return func

    return decorator


def register_two_argument_operation[Impls, Op, Impl](
        implementations: Impls,
        op: Op,
        first: TypeName,
        second: TypeName,
        implementation: Impl
):
    if op not in implementations:
        implementations[op] = {}

    if first not in implementations[op]:
        implementations[op][first] = {}

    if second in implementations[op][first]:
        raise OperationImplementationAlreadyRegisteredError(
            op.value,
            first,
            second
        )

    implementations[op][first][second] = implementation


class OperationsRegistry(Registrable):

    # region Dunder Methods

    def __init__(self):
        self._bool_implementations: Bool = {}
        self._compare_implementations: Compare = {}
        self._binary_implementations: Binary = {}
        self._unary_implementations: Unary = {}
        self._cast_implementations: Cast = {}

        super().__init__()

    # endregion

    # region Helpers

    def get_available_casts(self, type_name: TypeName) -> list[TypeName]:
        return list(self._cast_implementations.get(type_name, {}).keys())

    # endregion

    # region Operations

    def bool(self, op: EBoolOperationType, first: Value, second: Value) \
            -> Value:
        if not (implementations := self._bool_implementations.get(op, None)):
            raise MissingOperationImplementationError(
                op.to_operator(),
                first.type_name,
                second.type_name
            )

        if matching := implementations.get(first.type_name, None):
            if exact_operation := matching.get(second.type_name, None):
                return exact_operation(first, second)

        return self.bool(
            op,
            self.cast(first, BuiltinTypes.BOOL),
            self.cast(second, BuiltinTypes.BOOL)
        )

    def compare(self, op: ECompareType, first: Value, second: Value) \
            -> Value:
        return self._two_argument_operation(
            self._compare_implementations,
            op,
            first,
            second
        )

    def binary(self, op: EBinaryOperationType, first: Value, second: Value) \
            -> Value:
        return self._two_argument_operation(
            self._binary_implementations,
            op,
            first,
            second
        )

    def _two_argument_operation(
            self,
            implementations,
            op,
            first: Value,
            second: Value
    ) -> Value:
        if not (implementations := implementations.get(op, None)):
            raise MissingOperationImplementationError(
                op.to_operator(),
                first.type_name,
                second.type_name
            )

        if not (matching := implementations.get(first.type_name, None)):
            raise MissingOperationImplementationError(
                op.to_operator(),
                first.type_name,
                second.type_name
            )

        if exact_operation := matching.get(second.type_name, None):
            return exact_operation(first, second)

        for cast_type in self.get_available_casts(second.type_name):
            if cast_type in matching:
                second = self.cast(second, cast_type)
                return matching[cast_type](first, second)

        raise MissingOperationImplementationError(
            op.to_operator(),
            first.type_name,
            second.type_name
        )

    def unary(self, op: EUnaryOperationType, value: Value) -> Value:
        implementation = shall(
            self._unary_implementations.get(op, {}).get(value.type_name, None),
            MissingOperationImplementationError,
            f"unary {op.to_operator()}", value.type_name
        )

        return implementation(value)

    def cast(self, value: Value, to_type: TypeName) -> Value:
        if value.type_name.is_derived_from(to_type):
            return Value(
                type_name=to_type,
                value=value.value
            )

        implementation = shall(
            self._cast_implementations.get(value.type_name, {}) \
                .get(to_type, None),
            MissingOperationImplementationError,
            "cast", value.type_name, to_type
        )

        return implementation(value)

    def is_type(self, value: Value, is_type: TypeName) -> Value:
        if value.type_name.is_base_of(is_type):
            return Value(
                type_name=BuiltinTypes.BOOL,
                value=True
            )

        return Value(
            type_name=BuiltinTypes.BOOL,
            value=False
        )

    # endregion

    # region Registering

    def register_bool(
            self,
            op: EBoolOperationType,
            first: TypeName,
            second: TypeName,
            implementation: CompareImplementation
    ):
        register_two_argument_operation(
            self._bool_implementations,
            op,
            first,
            second,
            implementation
        )

    def register_compare(
            self,
            op: ECompareType,
            first: TypeName,
            second: TypeName,
            implementation: CompareImplementation
    ):
        register_two_argument_operation(
            self._compare_implementations,
            op,
            first,
            second,
            implementation
        )

    def register_binary(
            self,
            op: EBinaryOperationType,
            first: TypeName,
            second: TypeName,
            implementation: BinaryImplementation
    ):
        register_two_argument_operation(
            self._binary_implementations,
            op,
            first,
            second,
            implementation
        )

    def register_unary(
            self,
            op: EUnaryOperationType,
            type_name: TypeName,
            implementation: UnaryImplementation
    ):
        if op not in self._unary_implementations:
            self._unary_implementations[op] = {}

        if type_name in self._unary_implementations[op]:
            raise OperationImplementationAlreadyRegisteredError(
                f"unary {op.value}",
                type_name
            )

        self._unary_implementations[op][type_name] = implementation

    def register_cast(
            self,
            from_type: TypeName,
            to_type: TypeName,
            implementation: CastImplementation
    ):
        if from_type not in self._cast_implementations:
            self._cast_implementations[from_type] = {}

        if to_type in self._cast_implementations[from_type]:
            raise OperationImplementationAlreadyRegisteredError(
                "cast",
                from_type,
                to_type
            )

        self._cast_implementations[from_type][to_type] = implementation

    # endregion
