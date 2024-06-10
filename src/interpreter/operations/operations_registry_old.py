from src.interpreter.operations.operation_registry import OperationRegistry
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType


class OperationsRegistryOld:

    # region Dunder Methods

    def __init__(self):
        self.bool_operations = OperationRegistry[EBoolOperationType]()
        self.compare = OperationRegistry[ECompareType]()
        self.binary_operations = OperationRegistry[EBinaryOperationType]()
        self.unary_operations = OperationRegistry[EUnaryOperationType]()
        self.cast = OperationRegistry[str]()
        self.is_compare = OperationRegistry[str]()

    # endregion
