from collections import deque
from typing import Callable

from multimethod import multimethod

from src.common.box import Box
from src.common.position import Position
from src.interface.ivisitor import IVisitor
from src.interpreter.errors import InferenceError, EmptyVariableError, \
    VariableRedeclarationError, UndefinedFieldError, UndefinedStructError, \
    UndefinedVariableError, AssignmentTooConstantVariable, InvalidTypeError, \
    PanicBreak, PanicError, MissingOperationImplementationError, \
    EnumDefaultValueError
from src.interpreter.functions.functions_registry import FunctionsRegistry
from src.interpreter.functions.user_function_implementation import \
    UserFunctionImplementation
from src.interpreter.operations.operations_registry import OperationsRegistry
from src.interpreter.stack.frame import Frame
from src.interpreter.stack.value import Value
from src.interpreter.types.typename import TypeName
from src.interpreter.types.types_registry import TypesRegistry
from src.interpreter.visitors.name_visitor import NameVisitor
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.constant import Constant
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
from src.parser.interface.itree_like_expression import ITreeLikeExpression


class DynamicTypeValidator(IVisitor[Node]):

    # region Dunder Methods

    def __init__(
            self,
            types_registry: TypesRegistry,
            functions_registry: FunctionsRegistry,
            operations_registry: OperationsRegistry
    ):
        self._stack = deque()
        self._frame = Frame[str, tuple[bool, TypeName]]()
        self._type_name: Box[tuple[bool, TypeName]]() \
            = Box[tuple[bool, TypeName]]()

        self._return_value: Box[TypeName] = Box[TypeName]()

        self._name_visitor = NameVisitor()
        self._types_registry = types_registry
        self._functions_registry = functions_registry
        self._operations_registry = operations_registry

    # endregion

    def _register_visit(self, node: Node):
        self._stack.append(node)
        self.visit(node)
        self._stack.pop()

    # region Visits

    @multimethod
    def visit(self, module: Module) -> None:
        try:
            for function_declaration in module.function_declarations:
                self._register_visit(function_declaration)
        except PanicBreak as panic_break:
            position = Position(1, 1) \
                if len(self._stack) == 0 else self._stack[0].location.begin

            raise PanicError(
                panic_break.panic_message,
                position=position
            )
        except MissingOperationImplementationError as err:
            position = Position(1, 1) \
                if len(self._stack) == 0 else self._stack[0].location.begin
            err.position = position
            raise err

    @multimethod
    def visit(self, function_declaration: FunctionDeclaration) -> None:
        self._type_name.take()
        self.create_frame()

        self._name_visitor.visit(function_declaration.name)
        name = self._name_visitor.name.take()

        function_implementation = self._functions_registry.get_function(
            name
        )

        self._return_value.put(function_implementation.return_type)
        for name, (mutable, type_name) \
                in function_implementation.parameters.items():
            self._frame.set(
                name,
                (mutable, type_name)
            )

        self._register_visit(function_declaration.block)

        self.drop_frame()

    # endregion

    # region Frames Management

    def create_frame(self):
        self._frame = Frame(self._frame)

    def drop_frame(self):
        self._frame = self._frame.parent

    # endregion

    # region Visits - Statements

    @multimethod
    def visit(self, block: Block) -> None:
        self.create_frame()

        for statement in block.body:
            self._register_visit(statement)
            self._type_name.take()

        self.drop_frame()

    @multimethod
    def visit(self, variable_declaration: VariableDeclaration) -> None:
        # Get name
        self._name_visitor.visit(variable_declaration.name)
        name = self._name_visitor.name.take()

        # Get mutable state
        mutable = variable_declaration.mutable

        # Throw error if variable is already declared
        if self._frame.get(name, chain=False) is not None:
            raise VariableRedeclarationError(
                name,
                variable_declaration.location.begin
            )

        # Throw error if variable has no value and no declared_type
        if variable_declaration.declared_type is None \
                and variable_declaration.value is None:
            raise InferenceError(name, variable_declaration.location.begin)

        # Throw error if variable has no value and is constant
        if not mutable and variable_declaration.value is None:
            raise EmptyVariableError(name, variable_declaration.location.begin)

        declared_type_name = None
        if variable_declaration.declared_type:
            self._name_visitor.visit(variable_declaration.declared_type)
            declared_type_name = self._name_visitor.type.take()

        value_type_name = None
        if variable_declaration.value:
            self._register_visit(variable_declaration.value)
            _, value_type_name = self._type_name.take()

        if variable_declaration.declared_type \
                and not variable_declaration.value:
            impl = self._types_registry.get_type(declared_type_name)
            if not impl.can_instantiate():
                raise EnumDefaultValueError(
                    impl.as_type(),
                    variable_declaration.declared_type.location.begin
                )

        if declared_type_name is not None and value_type_name is not None:
            self._operations_registry.cast(
                Value(
                    type_name=value_type_name,
                    value=0
                ),
                declared_type_name
            )

        self._frame.set(
            name,
            (mutable, declared_type_name or value_type_name),
            chain=False
        )

    @multimethod
    def visit(self, assignment: Assignment) -> None:
        self._register_visit(assignment.access)
        mutable, type_name = self._type_name.take()

        if not mutable:
            raise AssignmentTooConstantVariable(
                assignment.location.begin
            )

        self._register_visit(assignment.value)
        _, value_type_name = self._type_name.take()

        self._operations_registry.cast(
            Value(type_name=value_type_name, value=0),
            type_name
        )

    @multimethod
    def visit(self, new_struct: NewStruct) -> None:
        self._name_visitor.visit(new_struct.variant)
        type_name = self._name_visitor.type.take()

        struct_impl = self._types_registry.get_struct(type_name)
        fields = {}

        for assignment in new_struct.assignments:
            self._name_visitor.visit(assignment.access)
            name = self._name_visitor.name.take()

            self._register_visit(assignment.value)
            _, assignment_type_name = self._type_name.take()

            if struct_impl.fields.get(name).as_type() != assignment_type_name:
                raise InvalidTypeError(
                    struct_impl.fields.get(name).as_type(),
                    assignment_type_name,
                    assignment.location.begin
                )

        self._type_name.put(
            (False, type_name)
        )

    @multimethod
    def visit(self, return_statement: ReturnStatement) -> None:
        expected = self._return_value.value()

        if return_statement.value is not None:
            self._register_visit(return_statement.value)

            _, type_name = self._type_name.take()
            if not expected.is_base_of(type_name):
                raise InvalidTypeError(
                    type_name,
                    expected,
                    return_statement.value.location.begin
                )

    @multimethod
    def visit(self, if_statement: IfStatement) -> None:
        self._register_visit(if_statement.condition)
        self._type_name.take()

        self._register_visit(if_statement.block)
        self._type_name.take()

        if if_statement.else_block:
            self._register_visit(if_statement.else_block)

    @multimethod
    def visit(self, while_statement: WhileStatement) -> None:
        self._register_visit(while_statement.condition)
        self._type_name.take()

        self._register_visit(while_statement.block)

    @multimethod
    def visit(self, match_statement: MatchStatement) -> None:
        self._register_visit(match_statement.expression)
        self._type_name.take()

        for matcher in match_statement.matchers:
            self._register_visit(matcher)

    @multimethod
    def visit(self, matcher: Matcher) -> None:
        self._name_visitor.visit(matcher.name)
        name = self._name_visitor.name.take()

        self._name_visitor.visit(matcher.checked_type)
        checked_type = self._name_visitor.type.take()

        self.create_frame()
        self._frame.set(
            name,
            (False, checked_type),
            chain=False
        )
        self._register_visit(matcher.block)
        self._type_name.take()
        self.drop_frame()

    @multimethod
    def visit(self, fn_call: FnCall) -> None:
        self._name_visitor.visit(fn_call.name)
        name = self._name_visitor.name.take()

        function_implementation = self._functions_registry.get_function(
            name
        )

        for argument, (_, declared_type) in zip(
                fn_call.arguments,
                function_implementation.parameters.values()
        ):
            self._register_visit(argument)
            _, argument_type_name = self._type_name.take()

            if argument_type_name != declared_type:
                raise InvalidTypeError(
                    argument_type_name,
                    declared_type,
                    argument.location.begin
                )

        self._type_name.put(
            (False, function_implementation.return_type)
        )

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
        _, left_type_name = self._type_name.take()
        self._register_visit(expression.right)
        _, right_type_name = self._type_name.take()

        self._type_name.put(
            (
                False,
                operation(
                    expression.op,
                    Value(type_name=left_type_name, value=0),
                    Value(type_name=right_type_name, value=0),
                ).type_name
            )
        )

    @multimethod
    def visit(self, expression: UnaryOperation) -> None:
        self._register_visit(expression.operand)
        _, type_name = self._type_name.take()

        self._type_name.put(
            (
                False,
                self._operations_registry.unary(
                    expression.op,
                    Value(type_name=type_name, value=0)
                ).type_name
            )
        )

    @multimethod
    def visit(self, expression: Cast) -> None:
        self._register_visit(expression.value)
        _, type_name = self._type_name.take()

        self._name_visitor.visit(expression.to_type)
        to_type = self._name_visitor.type.take()

        if not to_type.is_derived_from(type_name):
            self._operations_registry.cast(
                Value(type_name=type_name, value=0),
                to_type
            )

        self._type_name.put(
            (False, to_type)
        )

    @multimethod
    def visit(self, expression: IsCompare) -> None:
        self._register_visit(expression.value)
        _, type_name = self._type_name.take()

        self._name_visitor.visit(expression.is_type)
        is_type = self._name_visitor.type.take()

        result_type = self._operations_registry.is_type(
            Value(type_name=type_name, value=0),
            is_type
        ).type_name

        self._type_name.put(
            (False, result_type)
        )

    @multimethod
    def visit(self, constant: Constant) -> None:
        type_name = TypeName.parse(constant.type.to_name())
        self._type_name.put(
            (False, type_name)
        )

    # endregion

    # region Names

    @multimethod
    def visit(self, name: Name) -> None:
        if self._type_name.value():
            mutable, type_name = self._type_name.take()
            impl = self._types_registry.get_struct(type_name)

            if impl is None:
                raise UndefinedStructError(
                    name.identifier,
                    name.location.begin
                )

            if not (field := impl.fields.get(name.identifier)):
                raise UndefinedFieldError(name.identifier, name.location.begin)

            self._type_name.put(
                (mutable, field.as_type())
            )
        else:
            variable = self._frame.get(name.identifier)

            if not variable:
                raise UndefinedVariableError(
                    name.identifier,
                    name.location.begin
                )

            self._type_name.put(
                variable
            )

    @multimethod
    def visit(self, access: Access) -> None:
        self._register_visit(access.parent)
        self._register_visit(access.name)

    # endregion
