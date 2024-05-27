from dataclasses import dataclass
from typing import Optional

from src.parser.ast.common import Type
from src.parser.ast.declaration.declaration import Declaration
from src.parser.ast.name import Name
from src.parser.ast.declaration.parameter import Parameter
from src.parser.ast.statements.block import Block

type Parameters = list[Parameter]


@dataclass
class FunctionDeclaration(Declaration):
    name: Name
    parameters: Parameters
    return_type: Optional[Type]
    block: Block
