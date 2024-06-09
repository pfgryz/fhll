from src.common.location import Location
from src.common.position import Position
from src.interpreter.types.typename import TypeName
from src.interpreter.visitors.name_visitor import NameVisitor
from src.parser.ast.name import Name
from src.parser.ast.variant_access import VariantAccess


def test_name_visitor__visit_name():
    name = Name(
        identifier="Main",
        location=Location.at(Position(1, 1))
    )

    name_visitor = NameVisitor()

    name_visitor.visit(name)
    assert name_visitor.name.take() == "Main"

    name_visitor.visit(name)
    assert name_visitor.type.take() == TypeName.parse("Main")


def test_name_visitor__visit_variant_access():
    variant_access = VariantAccess(
        name=Name(
            identifier="Main",
            location=Location.at(Position(1, 1))
        ),
        parent=Name(
            identifier="Ui",
            location=Location.at(Position(1, 1))
        ),
        location=Location.at(Position(1, 1)),
    )

    name_visitor = NameVisitor()

    name_visitor.visit(variant_access)
    assert name_visitor.name.take() == "Main"

    name_visitor.visit(variant_access)
    assert name_visitor.type.take() == TypeName.parse("Ui::Main")
