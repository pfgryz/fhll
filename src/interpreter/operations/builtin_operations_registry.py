from src.interpreter.errors import PanicBreak
from src.interpreter.operations.operations_registry import OperationsRegistry, \
    unary_impl, cast_impl, binary_impl, compare_impl, bool_impl
from src.interpreter.stack.value import Value
from src.interpreter.types.builtin_types import BuiltinTypes
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType


class BuiltinOperationsRegistry(OperationsRegistry):

    # region Dunder Methods

    def __init__(self):
        super().__init__()

    # region Bool

    @staticmethod
    @bool_impl(EBoolOperationType.And, BuiltinTypes.I32, BuiltinTypes.I32)
    @bool_impl(EBoolOperationType.And, BuiltinTypes.F32, BuiltinTypes.F32)
    @bool_impl(EBoolOperationType.And, BuiltinTypes.STR, BuiltinTypes.STR)
    @bool_impl(EBoolOperationType.And, BuiltinTypes.BOOL, BuiltinTypes.BOOL)
    def _and_impl[T: int | float | str](first: Value[T], second: Value[T]) \
            -> Value[T]:

        return Value(
            type_name=first.type_name,
            value=first.value and second.value
        )

    @staticmethod
    @bool_impl(EBoolOperationType.Or, BuiltinTypes.I32, BuiltinTypes.I32)
    @bool_impl(EBoolOperationType.Or, BuiltinTypes.F32, BuiltinTypes.F32)
    @bool_impl(EBoolOperationType.Or, BuiltinTypes.STR, BuiltinTypes.STR)
    @bool_impl(EBoolOperationType.Or, BuiltinTypes.BOOL, BuiltinTypes.BOOL)
    def _or_impl[T: int | float | str](first: Value[T], second: Value[T]) \
            -> Value[T]:

        return Value(
            type_name=first.type_name,
            value=first.value or second.value
        )

    # endregion

    # region Compare

    @staticmethod
    @compare_impl(ECompareType.Equal, BuiltinTypes.I32, BuiltinTypes.I32)
    @compare_impl(ECompareType.Equal, BuiltinTypes.F32, BuiltinTypes.F32)
    @compare_impl(ECompareType.Equal, BuiltinTypes.STR, BuiltinTypes.STR)
    @compare_impl(ECompareType.Equal, BuiltinTypes.BOOL, BuiltinTypes.BOOL)
    def _eq_impl[T: int | float | str | bool] \
                    (first: Value[T], second: Value[T]) -> Value[bool]:
        return Value(
            type_name=BuiltinTypes.BOOL,
            value=first.value == second.value
        )

    @staticmethod
    @compare_impl(ECompareType.NotEqual, BuiltinTypes.I32, BuiltinTypes.I32)
    @compare_impl(ECompareType.NotEqual, BuiltinTypes.F32, BuiltinTypes.F32)
    @compare_impl(ECompareType.NotEqual, BuiltinTypes.STR, BuiltinTypes.STR)
    @compare_impl(ECompareType.NotEqual, BuiltinTypes.BOOL, BuiltinTypes.BOOL)
    def _neq_impl[T: int | float | str | bool] \
                    (first: Value[T], second: Value[T]) -> Value[bool]:
        return Value(
            type_name=BuiltinTypes.BOOL,
            value=first.value != second.value
        )

    @staticmethod
    @compare_impl(ECompareType.Less, BuiltinTypes.I32, BuiltinTypes.I32)
    @compare_impl(ECompareType.Less, BuiltinTypes.F32, BuiltinTypes.F32)
    def _lt_impl[T: int | float] \
                    (first: Value[T], second: Value[T]) -> Value[bool]:
        return Value(
            type_name=BuiltinTypes.BOOL,
            value=first.value < second.value
        )

    @staticmethod
    @compare_impl(ECompareType.Greater, BuiltinTypes.I32, BuiltinTypes.I32)
    @compare_impl(ECompareType.Greater, BuiltinTypes.F32, BuiltinTypes.F32)
    def _gt_impl[T: int | float] \
                    (first: Value[T], second: Value[T]) -> Value[bool]:
        return Value(
            type_name=BuiltinTypes.BOOL,
            value=first.value > second.value
        )

    # endregion

    # region Binary

    @staticmethod
    @binary_impl(EBinaryOperationType.Add, BuiltinTypes.I32, BuiltinTypes.I32)
    @binary_impl(EBinaryOperationType.Add, BuiltinTypes.F32, BuiltinTypes.F32)
    @binary_impl(EBinaryOperationType.Add, BuiltinTypes.STR, BuiltinTypes.STR)
    def _add_impl[T: int | float | str](first: Value[T], second: Value[T]) \
            -> Value[T]:
        return Value(
            type_name=first.type_name,
            value=first.value + second.value,
        )

    @staticmethod
    @binary_impl(EBinaryOperationType.Sub, BuiltinTypes.I32, BuiltinTypes.I32)
    @binary_impl(EBinaryOperationType.Sub, BuiltinTypes.F32, BuiltinTypes.F32)
    def _sub_impl[T: int | float](first: Value[T], second: Value[T]) \
            -> Value[T]:
        return Value(
            type_name=first.type_name,
            value=first.value - second.value,
        )

    @staticmethod
    @binary_impl(EBinaryOperationType.Multiply,
                 BuiltinTypes.I32, BuiltinTypes.I32)
    @binary_impl(EBinaryOperationType.Multiply,
                 BuiltinTypes.F32, BuiltinTypes.F32)
    def _mul_impl[T: int | float](first: Value[T], second: Value[T]) \
            -> Value[T]:
        return Value(
            type_name=first.type_name,
            value=first.value * second.value,
        )

    @staticmethod
    @binary_impl(EBinaryOperationType.Multiply,
                 BuiltinTypes.STR, BuiltinTypes.I32)
    def _div_impl[T: str, S: str](first: Value[T], second: Value[S]) \
            -> Value[T]:
        return Value(
            type_name=first.type_name,
            value=first.value * second.value
        )

    @staticmethod
    @binary_impl(EBinaryOperationType.Divide,
                 BuiltinTypes.I32, BuiltinTypes.I32)
    @binary_impl(EBinaryOperationType.Divide,
                 BuiltinTypes.F32, BuiltinTypes.F32)
    def _div_impl[T: int | float](first: Value[T], second: Value[T]) \
            -> Value[T]:
        if second.value == 0:
            raise PanicBreak("Trying divide by zero")

        return Value(
            type_name=first.type_name,
            value=first.value / second.value,
        )

    # endregion

    # region Unary

    @staticmethod
    @unary_impl(EUnaryOperationType.Minus, BuiltinTypes.I32)
    @unary_impl(EUnaryOperationType.Minus, BuiltinTypes.F32)
    def _unary_minus_impl[T: int | float](value: Value[T]) -> Value[T]:
        return Value(
            type_name=value.type_name,
            value=-value.value
        )

    @staticmethod
    @unary_impl(EUnaryOperationType.Negate, BuiltinTypes.BOOL)
    def _negate_impl(value: Value[bool]) -> Value[bool]:
        return Value(
            type_name=value.type_name,
            value=not value.value
        )

    # endregion

    # region Cast

    @staticmethod
    @cast_impl(BuiltinTypes.F32, BuiltinTypes.I32)
    @cast_impl(BuiltinTypes.STR, BuiltinTypes.I32)
    @cast_impl(BuiltinTypes.BOOL, BuiltinTypes.I32)
    def _i32_cast_impl(value: Value[float | bool | str]) -> Value[int]:
        try:
            parsed = int(value.value)
        except (ValueError, TypeError):
            raise PanicBreak("Cannot convert to i32")

        return Value(
            type_name=BuiltinTypes.I32,
            value=parsed
        )

    @staticmethod
    @cast_impl(BuiltinTypes.I32, BuiltinTypes.F32)
    @cast_impl(BuiltinTypes.STR, BuiltinTypes.F32)
    @cast_impl(BuiltinTypes.BOOL, BuiltinTypes.F32)
    def _f32_cast_impl(value: Value[int | bool | str]) -> Value[float]:
        try:
            parsed = float(value.value)
        except (ValueError, TypeError):
            raise PanicBreak("Cannot convert to f32")

        return Value(
            type_name=BuiltinTypes.F32,
            value=parsed
        )

    @staticmethod
    @cast_impl(BuiltinTypes.I32, BuiltinTypes.STR)
    @cast_impl(BuiltinTypes.F32, BuiltinTypes.STR)
    @cast_impl(BuiltinTypes.BOOL, BuiltinTypes.STR)
    def _str_cast_impl(value: Value[int | float | bool]) -> Value[str]:
        return Value(
            type_name=BuiltinTypes.STR,
            value=str(value.value)
        )

    @staticmethod
    @cast_impl(BuiltinTypes.I32, BuiltinTypes.BOOL)
    @cast_impl(BuiltinTypes.F32, BuiltinTypes.BOOL)
    @cast_impl(BuiltinTypes.STR, BuiltinTypes.BOOL)
    def _bool_cast_impl(value: Value[int | float | str]) -> Value[bool]:
        return Value(
            type_name=BuiltinTypes.BOOL,
            value=bool(value.value)
        )

    # endregion
