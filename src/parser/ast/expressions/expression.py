from abc import ABC

from src.parser.ast.node import Node


class Expression(Node, ABC):
    pass
