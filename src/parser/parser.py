import typing
from typing import Optional

from src.common.location import Location
from src.common.position import Position
from src.common.shall import shall
from src.lexer.lexer import Lexer
from src.lexer.token import Token
from src.lexer.token_kind import TokenKind
from src.parser.ast.access import Access
from src.parser.ast.cast import Cast
from src.parser.ast.common import Type
from src.parser.ast.constant import Constant, ConstantValueType
from src.parser.ast.declaration.enum_declaration import EnumDeclaration
from src.parser.ast.declaration.field_declaration import FieldDeclaration
from src.parser.ast.declaration.function_declaration import FunctionDeclaration
from src.parser.ast.declaration.parameter import Parameter
from src.parser.ast.declaration.struct_declaration import StructDeclaration
from src.parser.ast.expressions.binary_operation import BinaryOperation
from src.parser.ast.expressions.binary_operation_type import \
    EBinaryOperationType
from src.parser.ast.expressions.bool_operation import BoolOperation
from src.parser.ast.expressions.bool_operation_type import EBoolOperationType
from src.parser.ast.expressions.compare import Compare
from src.parser.ast.expressions.compare_type import ECompareType
from src.parser.ast.expressions.expression import Expression
from src.parser.ast.expressions.term import Term
from src.parser.ast.expressions.unary_operation import UnaryOperation
from src.parser.ast.expressions.unary_operation_type import EUnaryOperationType
from src.parser.ast.is_compare import IsCompare
from src.parser.ast.module import Module
from src.parser.ast.name import Name
from src.parser.ast.statements.assignment import Assignment
from src.parser.ast.statements.block import Block
from src.parser.ast.statements.fn_call import FnCall
from src.parser.ast.statements.if_statement import IfStatement
from src.parser.ast.statements.match_statement import MatchStatement
from src.parser.ast.statements.matcher import Matcher
from src.parser.ast.statements.new_struct_statement import NewStruct
from src.parser.ast.statements.return_statement import ReturnStatement
from src.parser.ast.statements.statement import Statement
from src.parser.ast.statements.variable_declaration import VariableDeclaration
from src.parser.ast.statements.while_statement import WhileStatement
from src.parser.ast.variant_access import VariantAccess
from src.parser.ebnf import ebnf
from src.parser.errors import TokenExpectedError, ParserError, \
    NameExpectedError, SemicolonExpectedError, ColonExpectedError, \
    BlockExpectedError, ParenthesisExpectedError, TypeExpectedError, \
    ParameterExpectedError, ExpressionExpectedError, LetKeywordExpectedError, \
    AssignExpectedError, BraceExpectedError, UnexpectedTokenError, \
    BoldArrowExpectedError, MatchersExpectedError
from src.parser.interface.ifrom_token_kind import IFromTokenKind
from src.parser.interface.itree_like_expression import ITreeLikeExpression

type SyntaxExceptionType = Optional[typing.Type[ParserError]]


class Parser:
    # region Language Definition (builtin-types_old)

    _builtin_types_kinds = [
        TokenKind.I32,
        TokenKind.F32,
        TokenKind.Bool,
        TokenKind.Str
    ]

    _literal_kinds = [
        TokenKind.Integer,
        TokenKind.Float,
        TokenKind.String,
        TokenKind.Boolean
    ]

    # endregion

    # region Language Definition (operators)

    _and_op = [
        TokenKind.And
    ]

    _or_op = [
        TokenKind.Or
    ]

    _relation_op = [
        TokenKind.Equal,
        TokenKind.NotEqual,
        TokenKind.Less,
        TokenKind.Greater
    ]

    _additive_op = [
        TokenKind.Plus,
        TokenKind.Minus
    ]

    _multiplicative_op = [
        TokenKind.Multiply,
        TokenKind.Divide
    ]

    _unary_op = [
        TokenKind.Minus,
        TokenKind.Negate
    ]

    # endregion

    # region Dunder Methods

    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._token = None
        self._last = None

        # Start consuming tokens
        if self._token is None:
            self.consume()

    # endregion

    # region Helper Methods

    def check_if(self, *kinds: TokenKind) -> bool:
        if self._token is None:
            return False

        return self._token.kind in kinds

    def consume(self) -> Token:
        token = self._token
        self._token = self._lexer.get_next_token()

        while not self._token or self._token.kind == TokenKind.Comment:
            self._token = self._lexer.get_next_token()

        return token

    def consume_if(self, *kinds: TokenKind) -> Optional[Token]:
        if self.check_if(*kinds):
            return self.consume()

        return None

    def expect(
            self, kinds: TokenKind | list[TokenKind], condition: bool = True,
            exception: SyntaxExceptionType = None
    ) -> Optional[Token]:
        if not isinstance(kinds, list):
            kinds = [kinds]

        if token := self.consume_if(*kinds):
            return token

        if condition:
            if exception:
                raise exception(self._token.location.begin)
            raise TokenExpectedError(
                kinds, self._token.kind, self._token.location.begin
            )

        return None

    # endregion

    # region Parse Module
    @ebnf(
        "Module",
        "{ FunctionDeclaration | StructDeclaration | EnumDeclaration }"
    )
    def parse(self) -> Module:
        function_declarations = []
        struct_declarations = []
        enum_declarations = []

        while True:
            if function_declaration := self.parse_function_declaration():
                function_declarations.append(function_declaration)
            elif struct_declaration := self.parse_struct_declaration():
                struct_declarations.append(struct_declaration)
            elif enum_declaration := self.parse_enum_declaration():
                enum_declarations.append(enum_declaration)
            else:
                break

        if (token := self.consume()) and token.kind != TokenKind.EOF:
            raise UnexpectedTokenError(token.location.begin)

        return Module(
            name="",
            path="",
            function_declarations=function_declarations,
            struct_declarations=struct_declarations,
            enum_declarations=enum_declarations,
            location=Location.at(Position(1, 1))
        )

    # endregion

    # region Parse Functions

    @ebnf(
        "FunctionDeclaration",
        "'fn', identifier, '(', [ Parameters ], ')', [ '->', Type ], Block"
    )
    def parse_function_declaration(self) -> Optional[FunctionDeclaration]:
        if not (fn_kw := self.consume_if(TokenKind.Fn)):
            return None

        name = shall(self.parse_name(), NameExpectedError, fn_kw.location.end)

        # Parameters
        self.expect(TokenKind.ParenthesisOpen,
                    exception=ParenthesisExpectedError)
        parameters = self.parse_parameters()
        close = self.expect(
            TokenKind.ParenthesisClose, exception=ParenthesisExpectedError
        )
        end = close.location.end

        # Return Type
        if returns := self.parse_function_declaration_return_type():
            end = returns.location.end

        block = shall(self.parse_block(), BlockExpectedError, end)

        return FunctionDeclaration(
            name=name,
            parameters=parameters,
            return_type=returns,
            block=block,
            location=Location(
                fn_kw.location.begin,
                end
            )
        )

    def parse_function_declaration_return_type(self) -> Optional[Type]:
        if not (arrow := self.consume_if(TokenKind.Arrow)):
            return None

        return shall(self.parse_type(), TypeExpectedError, arrow.location.end)

    @ebnf(
        "Parameters", "{ ',', Parameter }"
    )
    def parse_parameters(self) -> list[Parameter]:
        parameters = []

        if parameter := self.parse_parameter():
            parameters.append(parameter)

        while comma := self.consume_if(TokenKind.Comma):
            if parameter := self.parse_parameter():
                parameters.append(parameter)
            else:
                raise ParameterExpectedError(comma.location.end)

        return parameters

    @ebnf(
        "Parameter", "[ 'mut' ], identifier, ':', Type"
    )
    def parse_parameter(self) -> Optional[Parameter]:
        mut = self.consume_if(TokenKind.Mut)
        mutable = mut is not None

        if not (name := self.parse_name()):
            if mutable:
                raise NameExpectedError(mut.location.end)

            return None

        self.expect(TokenKind.Colon, exception=ColonExpectedError)

        typ = self.parse_type()

        return Parameter(
            name=name,
            declared_type=typ,
            mutable=mutable,
            location=Location(
                mut.location.begin if mutable else name.location.begin,
                typ.location.end
            )
        )

    # endregion

    # region Parse Structs

    @ebnf(
        "StructDeclaration",
        "'struct', identifier, '{', { FieldDeclaration }, '}'"
    )
    def parse_struct_declaration(self) -> Optional['StructDeclaration']:
        if not (struct_kw := self.consume_if(TokenKind.Struct)):
            return None

        name = shall(self.parse_name(), NameExpectedError,
                     struct_kw.location.end)

        self.expect(TokenKind.BraceOpen, exception=BraceExpectedError)

        fields = []
        while field := self.parse_field_declaration():
            fields.append(field)

        close = self.expect(TokenKind.BraceClose, exception=BraceExpectedError)

        return StructDeclaration(
            name=name,
            fields=fields,
            location=Location(
                struct_kw.location.begin,
                close.location.end
            )
        )

    @ebnf(
        "FieldDeclaration",
        "identifier, ':', Type, ';'"
    )
    def parse_field_declaration(self) -> Optional[FieldDeclaration]:
        if not (name := self.parse_name()):
            return None

        colon = self.expect(TokenKind.Colon, exception=ColonExpectedError)
        declared_type = shall(self.parse_type(), TypeExpectedError,
                              colon.location.end)
        self.expect(TokenKind.Semicolon, exception=SemicolonExpectedError)

        return FieldDeclaration(
            name=name,
            declared_type=declared_type,
            location=Location(name.location.begin, declared_type.location.end)
        )

    # endregion

    # region Parse Enum

    @ebnf(
        "EnumDeclaration",
        "'enum', identifier, "
        "'{', { (EnumDeclaration | StructDeclaration) }, '}'"
    )
    def parse_enum_declaration(self) -> Optional[EnumDeclaration]:
        if not (enum_kw := self.consume_if(TokenKind.Enum)):
            return None

        name = shall(self.parse_name(), NameExpectedError,
                     enum_kw.location.end)

        self.expect(TokenKind.BraceOpen, exception=BraceExpectedError)

        variants = []
        while variant := self.parse_struct_declaration() \
                         or self.parse_enum_declaration():
            variants.append(variant)
            self.expect(TokenKind.Semicolon, exception=SemicolonExpectedError)

        close = self.expect(TokenKind.BraceClose, exception=BraceExpectedError)

        return EnumDeclaration(
            name=name,
            variants=variants,
            location=Location(
                enum_kw.location.begin,
                close.location.end
            )
        )

    # endregion

    # region Parse Statements

    @ebnf(
        "Block",
        "'{', StatementList, '}'"
    )
    def parse_block(self) -> Optional[Block]:
        if not (open_paren := self.consume_if(TokenKind.BraceOpen)):
            return None

        statements = self.parse_statements_list()

        close_paren = self.expect(TokenKind.BraceClose,
                                  exception=BraceExpectedError)

        return Block(
            body=statements,
            location=Location(
                open_paren.location.begin,
                close_paren.location.end
            )
        )

    @ebnf(
        "StatementList",
        "{ (Statement, ';') | BlockStatement }"
    )
    def parse_statements_list(self) -> list[Statement]:
        statements = []

        parsed = True
        while parsed:
            if statement := self.parse_statement():
                statements.append(statement)
                self.expect(TokenKind.Semicolon,
                            exception=SemicolonExpectedError)
            elif statement := self.parse_block_statement():
                statements.append(statement)
            else:
                parsed = False

        return statements

    @ebnf(
        "Statement",
        "Declaration | Assignment | FnCall | ReturnStatement"
    )
    def parse_statement(self) -> Optional[Statement]:
        if declaration := self.parse_declaration():
            return declaration

        if return_statement := self.parse_return_statement():
            return return_statement

        """
        Conflict of first symbol for constructions:
            Assignment := Access, '=', Expression;
            Access := identifier, { '.', identifier };
            FnCall := identifier, '(', [ FnArguments ], ')';

        Solution:
            - identifier in Assignment is followed by '.' or '='
            - identifier in FnCall is followed by '('
            - otherwise unexpected token
        """
        if identifier := self.consume_if(TokenKind.Identifier):
            self._last = identifier
            if self.check_if(TokenKind.Period) \
                    or self.check_if(TokenKind.Assign):
                assignment = self.parse_assignment()
                return assignment

            if self.check_if(TokenKind.ParenthesisOpen):
                fn_call = self.parse_fn_call()
                return fn_call

            raise UnexpectedTokenError(identifier.location.begin)

        return None

    @ebnf(
        "BlockStatement",
        "Block | IfStatement | WhileStatement | MatchStatement"
    )
    def parse_block_statement(self) -> Optional[Statement]:
        return self.parse_block() \
            or self.parse_if_statement() \
            or self.parse_while_statement() \
            or self.parse_match_statement()

    @ebnf(
        "Declaration",
        "[ 'mut' ], 'let', identifier, [ ':', Type ], [ '=', Expression ]"
    )
    def parse_declaration(self) -> Optional[VariableDeclaration]:
        mut = self.consume_if(TokenKind.Mut)

        if not (let := self.expect(
                TokenKind.Let, mut is not None, LetKeywordExpectedError
        )):
            return None

        begin = let.location.begin if mut is None else mut.location.begin

        name = shall(self.parse_name(), NameExpectedError, let.location.end)
        end = name.location.end

        if types := self.parse_declaration_type():
            end = types.location.end

        if value := self.parse_declaration_value():
            end = value.location.end

        return VariableDeclaration(
            name=name,
            mutable=mut is not None,
            declared_type=types,
            value=value,
            location=Location(
                begin,
                end
            )
        )

    def parse_declaration_type(self) -> Optional[Type]:
        if not (colon := self.consume_if(TokenKind.Colon)):
            return None

        return shall(self.parse_type(), TypeExpectedError, colon.location.end)

    def parse_declaration_value(self) -> Optional[Expression]:
        if not (assign := self.consume_if(TokenKind.Assign)):
            return None

        return shall(self.parse_expression(), ExpressionExpectedError,
                     assign.location.end)

    @ebnf(
        "Assignment",
        "Access, '=', Expression"
    )
    def parse_assignment(self) -> Optional[Assignment]:
        if not (access := self.parse_access()):
            return None

        assign = self.expect(TokenKind.Assign, exception=AssignExpectedError)

        if not (value := self.parse_expression()):
            raise ExpressionExpectedError(assign.location.end)

        return Assignment(
            access=access,
            value=value,
            location=Location(
                access.location.begin,
                value.location.end
            )
        )

    @ebnf(
        "FnCall",
        "identifier, '(', [ FnArguments ], ')'"
    )
    def parse_fn_call(self) -> Optional[FnCall]:
        if not (name := self.parse_name()):
            return None

        self.expect(TokenKind.ParenthesisOpen,
                    exception=ParenthesisExpectedError)
        arguments = self.parse_fn_arguments()
        close = self.expect(
            TokenKind.ParenthesisClose, exception=ParenthesisExpectedError
        )

        return FnCall(
            name=name,
            arguments=arguments,
            location=Location(
                name.location.begin,
                close.location.end
            )
        )

    @ebnf(
        "FnArguments",
        "Expression, {, ',', Expression }"
    )
    def parse_fn_arguments(self) -> list[Expression]:
        arguments = []

        if not (expression := self.parse_expression()):
            return arguments

        arguments.append(expression)

        while comma := self.consume_if(TokenKind.Comma):
            expression = shall(self.parse_expression(),
                               ExpressionExpectedError, comma.location.end)

            arguments.append(expression)

        return arguments

    @ebnf(
        "NewStruct",
        "VariantAccess, '{', { Assignment, ';' }, '}'"
    )
    def parse_new_struct(self) -> Optional[NewStruct]:
        if not (variant_access := self.parse_variant_access()):
            return None

        self.expect(TokenKind.BraceOpen, exception=BraceExpectedError)

        assignments = []

        while assignment_statement := self.parse_assignment():
            assignments.append(assignment_statement)
            self.expect(TokenKind.Semicolon, exception=SemicolonExpectedError)

        close = self.expect(TokenKind.BraceClose, exception=BraceExpectedError)

        return NewStruct(
            variant=variant_access,
            assignments=assignments,
            location=Location(
                variant_access.location.begin,
                close.location.end
            )
        )

    @ebnf(
        "ReturnStatement",
        "'return', [ Expression ]"
    )
    def parse_return_statement(self) -> Optional[ReturnStatement]:
        if not (return_kw := self.consume_if(TokenKind.Return)):
            return None

        value = None
        if expression := self.parse_expression():
            value = expression

        return ReturnStatement(
            value=value,
            location=Location(
                return_kw.location.begin,
                return_kw.location.end if value is None else value.location.end
            )
        )

    @ebnf(
        "IfStatement",
        "'if', '(', Expression, ')', Block, [ 'else', Block ]"
    )
    def parse_if_statement(self) -> Optional[IfStatement]:
        if not (if_kw := self.consume_if(TokenKind.If)):
            return None

        open_paren = self.expect(
            TokenKind.ParenthesisOpen, exception=ParenthesisExpectedError
        )

        condition = shall(self.parse_expression(), ExpressionExpectedError,
                          open_paren.location.end)

        close_paren = self.expect(
            TokenKind.ParenthesisClose, exception=ParenthesisExpectedError
        )

        else_block = None
        block = shall(self.parse_block(), BlockExpectedError,
                      close_paren.location.end)
        end = block.location.end

        if else_kw := self.consume_if(TokenKind.Else):
            else_block = shall(self.parse_block(), BlockExpectedError,
                               else_kw.location.end)

            end = else_block.location.end

        return IfStatement(
            condition=condition,
            block=block,
            else_block=else_block,
            location=Location(
                if_kw.location.begin,
                end
            )
        )

    @ebnf(
        "WhileStatement",
        "'while', '(', Expression, ')', Block"
    )
    def parse_while_statement(self) -> Optional[WhileStatement]:
        if not (while_kw := self.consume_if(TokenKind.While)):
            return None

        open_paren = self.expect(
            TokenKind.ParenthesisOpen, exception=ParenthesisExpectedError
        )

        condition = shall(self.parse_expression(), ExpressionExpectedError,
                          open_paren.location.end)

        close = self.expect(TokenKind.ParenthesisClose,
                            exception=ParenthesisExpectedError)

        block = shall(self.parse_block(), BlockExpectedError,
                      close.location.end)

        return WhileStatement(
            condition=condition,
            block=block,
            location=Location(
                while_kw.location.begin,
                block.location.end
            )
        )

    @ebnf(
        "MatchStatement",
        "'match', '(', Expression, ')', '{', Matchers, '}'"
    )
    def parse_match_statement(self) -> Optional[MatchStatement]:
        if not (match_kw := self.consume_if(TokenKind.Match)):
            return None

        open_paren = self.expect(
            TokenKind.ParenthesisOpen, exception=ParenthesisExpectedError
        )
        expression = shall(self.parse_expression(), ExpressionExpectedError,
                           open_paren.location.end)
        self.expect(
            TokenKind.ParenthesisClose, exception=ParenthesisExpectedError
        )

        open_brace = self.expect(TokenKind.BraceOpen,
                                 exception=BraceExpectedError)
        matchers = shall(self.parse_matchers(), MatchersExpectedError,
                         open_brace.location.end)
        close_brace = self.expect(TokenKind.BraceClose,
                                  exception=BraceExpectedError)

        return MatchStatement(
            expression=expression,
            matchers=matchers,
            location=Location(
                match_kw.location.begin,
                close_brace.location.end
            )
        )

    @ebnf(
        "Matchers",
        "Matcher, { Matcher }"
    )
    def parse_matchers(self) -> Optional[list[Matcher]]:
        if not (matcher := self.parse_matcher()):
            return None

        matchers = [matcher]

        while matcher := self.parse_matcher():
            matchers.append(matcher)

        return matchers

    @ebnf(
        "Matcher",
        "Type, Name, '=>', Block, ';'"
    )
    def parse_matcher(self) -> Optional[Matcher]:
        if not (checked_type := self.parse_type()):
            return None

        name = shall(self.parse_name(), NameExpectedError,
                     checked_type.location.end)

        bold_arrow = self.expect(TokenKind.BoldArrow,
                                 exception=BoldArrowExpectedError)
        block = shall(self.parse_block(), BlockExpectedError,
                      bold_arrow.location.end)

        self.expect(TokenKind.Semicolon, exception=SemicolonExpectedError)

        return Matcher(
            checked_type=checked_type,
            name=name,
            block=block,
            location=Location(
                checked_type.location.begin,
                block.location.end
            )
        )

    # endregion

    # region Parse Access

    def parse_name(self) -> Optional[Name]:
        if self._last is not None:
            identifier = self._last
            self._last = None
        else:
            identifier = self.consume_if(TokenKind.Identifier)

        if not identifier:
            return None

        return Name(
            identifier=identifier.value,
            location=identifier.location
        )

    @ebnf(
        "Access",
        "identifier, { '.', identifier }"
    )
    def parse_access(self) -> Optional[Name | Access]:
        access = self.parse_name()

        if not access:
            return None

        while self.consume_if(TokenKind.Period):
            name = shall(self.parse_name(), NameExpectedError,
                         access.location.end)

            access = Access(
                name=name,
                parent=access,
                location=Location(access.location.begin, name.location.end)
            )

        return access

    @ebnf(
        "VariantAccess",
        "identifier, { '::', identifier }"
    )
    def parse_variant_access(self) -> Optional[Name | VariantAccess]:
        access = self.parse_name()

        if not access:
            return None

        while self.consume_if(TokenKind.DoubleColon):
            name = shall(self.parse_name(), NameExpectedError,
                         access.location.end)

            access = VariantAccess(
                name=name,
                parent=access,
                location=Location(access.location.begin, name.location.end)
            )

        return access

    @ebnf(
        "Type",
        "builtin_type | VariantAccess"
    )
    def parse_type(self) -> Optional[Type]:
        if builtin := self.consume_if(*self._builtin_types_kinds):
            return Name(
                identifier=builtin.kind.value,
                location=builtin.location
            )

        return self.parse_variant_access()

    # endregion

    # region Parse Expressions

    @ebnf(
        "Expression",
        "AndExpression, { or_op, AndExpression }"
    )
    def parse_expression(self) -> Optional[Expression]:
        return self._parse_tree_like_expression(
            BoolOperation,
            EBoolOperationType,
            self._or_op,
            self.parse_and_expression
        )

    @ebnf(
        "AndExpression",
        "RelationExpression, { and_op, RelationExpression }"
    )
    def parse_and_expression(self) -> Optional[Expression]:
        return self._parse_tree_like_expression(
            BoolOperation,
            EBoolOperationType,
            self._and_op,
            self.parse_relation_expression
        )

    @ebnf(
        "RelationExpression",
        "AdditiveTerm, [ relation_op, AdditiveTerm ]"
    )
    def parse_relation_expression(self) -> Optional[Expression]:
        left = self.parse_additive_term()

        if op := self.consume_if(*self._relation_op):
            right = shall(self.parse_additive_term(), ExpressionExpectedError,
                          op.location.end)

            left = Compare(
                left=left,
                right=right,
                op=ECompareType.from_token_kind(op.kind),
                location=Location(
                    left.location.begin,
                    right.location.end
                )
            )

        return left

    @ebnf(
        "AdditiveTerm",
        "MultiplicativeTerm, { additive_op, MultiplicativeTerm }"
    )
    def parse_additive_term(self) -> Optional[Expression]:
        return self._parse_tree_like_expression(
            BinaryOperation,
            EBinaryOperationType,
            self._additive_op,
            self.parse_multiplicative_term
        )

    @ebnf(
        "MultiplicativeTerm",
        "UnaryTerm, { multiplicative_op, UnaryTerm }"
    )
    def parse_multiplicative_term(self) -> Optional[Expression]:
        return self._parse_tree_like_expression(
            BinaryOperation,
            EBinaryOperationType,
            self._multiplicative_op,
            self.parse_unary_term
        )

    def _parse_tree_like_expression[T: ITreeLikeExpression, K: IFromTokenKind](
            self, base: typing.Type[T], parent_type: typing.Type[K],
            operators: list[TokenKind], child: typing.Callable
    ) -> T:
        left = child()

        while op := self.consume_if(*operators):
            right = shall(child(), ExpressionExpectedError, op.location.end)

            left = base(
                left=left,
                right=right,
                op=parent_type.from_token_kind(op.kind),
                location=Location(
                    left.location.begin,
                    right.location.end
                )
            )

        return left

    @ebnf(
        "UnaryTerm",
        "[ unary_op ], CastedTerm"
    )
    def parse_unary_term(self) -> Optional[Expression]:
        if op := self.consume_if(*self._unary_op):
            term = shall(self.parse_casted_term(), ExpressionExpectedError,
                         op.location.end)

            return UnaryOperation(
                operand=term,
                op=EUnaryOperationType.from_token_kind(op.kind),
                location=Location(
                    op.location.begin,
                    term.location.end
                )
            )

        return self.parse_casted_term()

    @ebnf(
        "CastedTerm",
        "Term, [ 'is', Type ], [ 'as', Type ]"
    )
    def parse_casted_term(self) -> Optional[Term]:
        if not (term := self.parse_term()):
            return None

        if as_kw := self.consume_if(TokenKind.As):
            to_type = shall(self.parse_type(), TypeExpectedError,
                            as_kw.location.end)

            return Cast(
                value=term,
                to_type=to_type,
                location=Location(term.location.begin, to_type.location.end)
            )

        if is_kw := self.consume_if(TokenKind.Is):
            to_type = shall(self.parse_type(), TypeExpectedError,
                            is_kw.location.end)

            return IsCompare(
                value=term,
                is_type=to_type,
                location=Location(term.location.begin, to_type.location.end)
            )

        return term

    @ebnf(
        "Term",
        "literal | Access"
        "| FnCall | NewStruct | '(', Expression, ')'"
    )
    def parse_term(self) -> Optional[Term]:
        if literal := self.consume_if(*self._literal_kinds):
            return Constant(
                value=literal.value,
                type=ConstantValueType.from_token_kind(literal.kind),
                location=literal.location
            )

        if open_paren := self.consume_if(TokenKind.ParenthesisOpen):
            expression = shall(self.parse_expression(),
                               ExpressionExpectedError,
                               open_paren.location.end)

            self.expect(TokenKind.ParenthesisClose,
                        exception=ParenthesisExpectedError)

            return expression

        """
        Conflict of first symbol for constructions:
            Access := identifier, { '.', identifier };
            FnCall := identifier, '(', [ FnArguments ], ')';
            NewStruct := VariantAccess, '{', { Assignment, ';' }, '}'
            VariantAccess := identifier, { '::', identifier };

        Solution:
            - identifier in NewStruct is followed by ':' or '{'
            - identifier in FnCall is followed by '('
            - identifier in Access can be single or followed by '.'
        """
        if identifier := self.consume_if(TokenKind.Identifier):
            self._last = identifier

            if self.check_if(TokenKind.DoubleColon) \
                    or self.check_if(TokenKind.BraceOpen):
                return self.parse_new_struct()
            elif self.check_if(TokenKind.ParenthesisOpen):
                return self.parse_fn_call()
            else:
                return self.parse_access()

        return None

    # endregion
