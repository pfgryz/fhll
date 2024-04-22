import warnings
from pprint import pprint
from typing import Optional

from src.lexer.lexer import Lexer
from src.lexer.token import Token
from src.lexer.token_kind import TokenKind
from src.parser.ast.access import Access
from src.parser.ast.name import Name
from src.parser.ast.program import Program
from src.parser.ast.variant_access import VariantAccess
from src.parser.ebnf import ebnf
from src.parser.errors import SyntaxExpectedTokenException
from src.utils.buffer import StreamBuffer


def untested():
    def wrapper(func):
        warnings.warn(f"This function {func.__name__} is not tested")
        return func

    return wrapper


class Parser:
    _builtin_types = [
        TokenKind.I32,
        TokenKind.F32,
        TokenKind.Bool,
        TokenKind.Str
    ]

    # region Dunder Methods
    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._token = None

    # endregion

    # region Helper Methods

    def consume(self) -> Token:
        token = self._token
        self._token = self._lexer.get_next_token()
        return token

    def consume_if(self, kind: TokenKind) -> Optional[Token]:
        if self._token.kind == kind:
            return self.consume()

        return None

    def consume_match(self, kinds: list[TokenKind]) -> Optional[Token]:
        for kind in kinds:
            if token := self.consume_if(kind):
                return token

        return None

    def expect(self, kind: TokenKind) -> Token:
        return self.expect_conditional(kind, True)

    def expect_conditional(self, kind: TokenKind, condition: bool) \
            -> Optional[Token]:
        if token := self.consume_if(kind):
            return token

        if condition:
            raise SyntaxExpectedTokenException(kind, self._token.kind,
                                               self._token.location.begin)

        return None

    def expect_match(self, kinds: list[TokenKind]) -> Optional[Token]:
        if token := self.consume_match(kinds):
            return token

        raise SyntaxExpectedTokenException(kinds, self._token.kind,
                                           self._token.location.begin)

    # endregion

    # region Parse Methods

    @ebnf(
        "Program",
        "{ FunctionDeclaration | StructDeclaration | EnumDeclaration }"
    )
    @untested()
    def parse(self) -> 'Program':
        raise NotImplementedError()

    # region Parse Functions

    @ebnf(
        "FunctionDeclaration",
        "'fn', identifier, '(', [ Parameters ], ')', [ '->', Type ], Block"
    )
    @untested()
    def parse_function_declaration(self) -> Optional['FunctionDeclaration']:
        raise NotImplementedError()

    @ebnf(
        "Parameters", "{ ',', Parameter }"
    )
    @untested()
    def parse_parameters(self) -> Optional['Parameters']:
        raise NotImplementedError()

    @ebnf(
        "Parameter", "[ 'mut' ], identifier, ':', Type"
    )
    @untested()
    def parse_parameter(self) -> Optional['Parameter']:
        raise NotImplementedError()

    # endregion

    # region Parse Structs

    @ebnf(
        "StructDeclaration",
        "'struct', identifier, '{', { FieldDeclaration }, '}'"
    )
    @untested()
    def parse_struct_declaration(self) -> Optional['StructDeclaration']:
        raise NotImplementedError()

    @ebnf(
        "FieldDeclaration",
        "identifier, ':', Type, ';'"
    )
    @untested()
    def parse_field_declaration(self) -> Optional['FieldDeclaration']:
        raise NotImplementedError()

    # endregion

    # region Parse Enum

    @ebnf(
        "EnumDeclaration",
        "'enum', identifier, '{', { VariantDeclaration }, '}'"
    )
    @untested()
    def parse_enum_declaration(self) -> Optional['EnumDeclaration']:
        raise NotImplementedError()

    @ebnf(
        "VariantDeclaration",
        "identifier, '{', { FieldDeclaration }, '}'"
    )
    @untested()
    def parse_variant_declaration(self) -> Optional['VariantDeclaration']:
        raise NotImplementedError()

    # endregion

    # region Parse Statements

    @ebnf(
        "Block",
        "'{', StatementList, '}'"
    )
    @untested()
    def parse_block(self) -> Optional['Block']:
        raise NotImplementedError()

    @ebnf(
        "StatementList",
        "{ Statement, ';'}"
    )
    @untested()
    def parse_statements_list(self) -> list['Statement']:
        raise NotImplementedError()

    @ebnf(
        "Statement",
        "Declaration | Assignment | FnCall | NewStruct "
        "| Block | ReturnStatement | IfStatement | WhileStatement"
    )
    @untested()
    def parse_statement(self) -> Optional['Statement']:
        raise NotImplementedError()

    @ebnf(
        "Declaration",
        "[ 'mut' ], 'let', identifier, [ ':', Type ], [ '=', Expression ]"
    )
    @untested()
    def parse_declaration(self) -> Optional['Declaration']:
        raise NotImplementedError()

    @ebnf(
        "Assignment",
        "Access, '=', Expression"
    )
    @untested()
    def parse_assignment(self) -> Optional['Assignment']:
        raise NotImplementedError()

    @ebnf(
        "FnCall",
        "identifier, '(', [ FnArguments ], ')'"
    )
    @untested()
    def parse_fn_call(self) -> Optional['FnCall']:
        raise NotImplementedError()

    @ebnf(
        "FnArguments",
        "Expression, {, ',', Expression }"
    )
    @untested()
    def parse_fn_arguments(self) -> list['FnArgument']:
        raise NotImplementedError()

    @ebnf(
        "NewStruct",
        "VariantAccess, '{', [ Assignment, ';' ], '}'"
    )
    @untested()
    def parse_new_struct(self) -> Optional['NewStruct']:
        pass

    @ebnf(
        "ReturnStatement",
        "'return', [ Expression ]"
    )
    @untested()
    def parse_return_statement(self) -> Optional['ReturnStatement']:
        raise NotImplementedError()

    @ebnf(
        "IfStatement",
        "'if', '(', Expression, ')', Block, [ 'else', Block ]"
    )
    @untested()
    def parse_if_statement(self) -> Optional['IfStatement']:
        raise NotImplementedError()

    @ebnf(
        "WhileStatement",
        "'while', '(', Expression, ')', Block"
    )
    @untested()
    def parse_while_statement(self) -> Optional['WhileStatement']:
        raise NotImplementedError()

    # endregion

    # region Parse Access

    @ebnf(
        "Access",
        "identifier, { '.', identifier }"
    )
    def parse_access(self) -> Optional[Name | Access]:
        if not (element := self.consume_if(TokenKind.Identifier)):
            return None

        result = Name(element.value, element.location)

        while self.consume_if(TokenKind.Comma):
            element = self.expect(TokenKind.Identifier)

            result = Access(
                Name(element.value, element.location),
                result
            )

        return result

    @ebnf(
        "VariantAccess",
        "identifier, { '::', identifier }"
    )
    @untested()
    def parse_variant_access(self) -> Optional[Name | VariantAccess]:
        if not (element := self.consume_if(TokenKind.Identifier)):
            return None

        result = Name(element.value, element.location)

        while self.consume_if(TokenKind.DoubleColon):
            element = self.expect(TokenKind.Identifier)

            result = VariantAccess(
                Name(element.value, element.location),
                result
            )

        return result

    @ebnf(
        "Type",
        "builtin_type | VariantAccess"
    )
    @untested()
    def parse_type(self) -> Optional['Type']:
        raise NotImplementedError()

    # endregion

    # region Parse Expressions

    @ebnf(
        "Expression",
        "AndExpression, { or_op, AndExpression }"
    )
    @untested()
    def parse_expression(self) -> Optional['Expression']:
        raise NotImplementedError()

    @ebnf(
        "AndExpression",
        "RelationExpression, { and_op, RelationExpression }"
    )
    @untested()
    def parse_and_expression(self) -> Optional['Expression']:
        raise NotImplementedError()

    @ebnf(
        "RelationExpression",
        "AdditiveTerm, { relation_op, AdditiveTerm }"
    )
    @untested()
    def parse_relation_expression(self) -> Optional['Expression']:
        raise NotImplementedError()

    @ebnf(
        "AdditiveTerm",
        "MultiplicativeTerm, { additive_op, MultiplicativeTerm }"
    )
    @untested()
    def parse_multiplicative_term(self) -> Optional['Expression']:
        raise NotImplementedError()

    @ebnf(
        "MultiplicativeTerm",
        "UnaryTerm, { multiplicative_op, UnaryTerm }"
    )
    @untested()
    def parse_multiplicative_term(self) -> Optional['Expression']:
        raise NotImplementedError()

    @ebnf(
        "UnaryTerm",
        "[ unary_op ], Term"
    )
    @untested()
    def parse_unary_term(self) -> Optional['Expression']:
        raise NotImplementedError()

    @ebnf(
        "Term",
        "literal | Access, [ 'is', Type ], [ 'as', Type ] "
        "| FnCall | NewStruct | '(', Expression, ')'"
    )
    @untested()
    def parse_term(self) -> Optional['Expression']:
        raise NotImplementedError()

    # endregion

    #
    # @ebnf("Program ::== "
    #       "{ FunctionDeclaration | StructDeclaration | EnumDeclaration }")
    # @untested()
    # def parse(self) -> Program:
    #     functions = {}
    #     structs = {}
    #
    #     # Read first token
    #     self.consume()
    #
    #     if function := self.parse_function():
    #         if functions.get(function.name) is not None:
    #             raise Exception(f"Double def")
    #
    #         functions[function.name] = function
    #
    #     if struct := self._parse_struct_declaration():
    #         if structs.get(struct.name) is not None:
    #             raise Exception(f"Double def struct")
    #
    #         structs[struct.name] = struct
    #
    #     return Program(
    #         functions,
    #         structs
    #     )
    #
    # #   = = = = = FUNCTION DECLARATION = = = = =
    # @ebnf("FunctionDeclaration ::== "
    #       "'fn', identifier, '(', [ Parameters ], ')', "
    #       "[ '->', Type ], Block")
    # @untested()
    # def parse_function(self) -> Optional[FunctionDeclaration]:
    #     if not self.consume_if(TokenKind.Fn):
    #         return None
    #
    #     name = self.expect(TokenKind.Identifier).value
    #     self.expect(TokenKind.ParenthesisOpen)
    #     parameters = self.parse_parameters()
    #     self.expect(TokenKind.ParenthesisClose)
    #
    #     returns = None
    #     if self.consume_if(TokenKind.Arrow):
    #         returns = self.consume().kind.value  # self._parse_type
    #
    #     block = []  # self._parse_block()
    #
    #     return FunctionDeclaration(
    #         name,
    #         parameters,
    #         returns,
    #         block
    #     )
    #
    # @ebnf("Parameters ::== Parameter, { ',', Parameter")
    # @untested()
    # def parse_parameters(self) -> list[Parameter]:
    #     parameters = []
    #
    #     if parameter := self.parse_parameter():
    #         parameters.append(parameter)
    #
    #     while self.consume_if(TokenKind.Period):
    #         if parameter := self.parse_parameter():
    #             parameters.append(parameter)
    #         else:
    #             raise SyntaxException("Expected parameter",
    #                                   self._token.location.begin)
    #
    #     return parameters
    #
    # @ebnf("Parameter ::== [ 'mut' ], identifier, ':', Type")
    # @untested()
    # def parse_parameter(self) -> Optional[Parameter]:
    #     mut = self.consume_if(TokenKind.Mut)
    #
    #     if not (identifier := self.expect_conditional(TokenKind.Identifier,
    #                                                   mut is not None)):
    #         return None
    #
    #     self.expect(TokenKind.Colon)
    #     types = self.consume().kind.value  # self._parse_type
    #
    #     return Parameter(
    #         identifier.value,
    #         types,
    #         mut is not None
    #     )
    #
    # #   = = = = = STRUCT DECLARATION = = = = =
    # @ebnf("StructDeclaration ::== "
    #       "'struct', identifier, '{', { FieldDeclaration }, '}'")
    # @untested()
    # def _parse_struct_declaration(self) -> Optional[StructDeclaration]:
    #     if not self.consume_if(TokenKind.Struct):
    #         return None
    #
    #     identifier = self.expect(TokenKind.Identifier)
    #     self.expect(TokenKind.BraceOpen)
    #
    #     fields = {}
    #     while field := self._parse_field_declaration():
    #         fields[field.name] = field
    #
    #     self.expect(TokenKind.BraceClose)
    #
    #     return StructDeclaration(
    #         identifier.value,
    #         fields
    #     )
    #
    # @ebnf("FieldDeclaration ::== identifier, ':', Type, ';'")
    # @untested()
    # def _parse_field_declaration(self) -> Optional[FieldDeclaration]:
    #     if not (identifier := self.consume_if(TokenKind.Identifier)):
    #         return None
    #
    #     self.expect(TokenKind.Colon)
    #     types = self.consume().kind.value  # self._parse_type
    #     self.expect(TokenKind.Semicolon)
    #
    #     return FieldDeclaration(
    #         identifier.value,
    #         types
    #     )
    #     pass
    #
    # endregion


if __name__ == "__main__":
    lexer = Lexer(StreamBuffer.from_str(
        # "fn main(x: i32, mut y: f32) { }"
        "struct Player { health: i32; }"
    ))
    parser = Parser(lexer)
    program = parser.parse()

    pprint(program)
