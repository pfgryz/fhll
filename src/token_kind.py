from enum import Enum, auto


class TokenKind(Enum):
    # Builtin Types
    U16 = "u16"
    U32 = "u32"
    U64 = "u64"
    I16 = "i16"
    I32 = "i32"
    I64 = "i64"
    F32 = "f32"
    Bool = "bool"
    Str = "str"

    # Keywords
    Fn = "fn"
    Struct = "struct"
    Enum = "enum"
    Mut = "mut"
    Let = "let"
    Is = "is"
    If = "if"
    While = "while"
    Return = "return"
    As = "as"
    Match = "match"

    # Literals
    Float = "float"
    Integer = "integer"
    String = "string"
    Boolean = "boolean"
    Identifier = "identifier"

    # Boolean Operators
    And = "&&"
    Or = "||"
    Negate = "!"

    # Relation Operators
    Equal = "=="
    NotEqual = "!="
    Greater = ">"
    Less = "<"

    # Arithmetic Operators
    Plus = "+"
    Minus = "-"
    Multiply = "*"
    Divide = "/"

    # Brackets
    ParenthesesOpen = "("
    ParenthesisClose = ")"
    BraceOpen = "{"
    BraceClose = "}"

    # Annotations
    TypeAnnotation = ":"
    ReturnTypeAnnotation = "->"

    # Access
    FieldAccess = "."
    VariantAccess = "::"

    # Other
    Matcher = "=>"
    Assign = "="
    Period = ","
    Separator = ";"

    Invalid = "<invalid>"
    EOF = "<eof>"
