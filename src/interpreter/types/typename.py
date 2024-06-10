import itertools

from src.interpreter.types.pathlike import PathLike


class TypeName(PathLike):
    symbol = "::"

    def is_derived_from(self, other: 'TypeName') -> bool:
        if not isinstance(other, TypeName):
            return False

        for derived, base in itertools.zip_longest(self.path, other.path):
            # Base should be shorter than derived
            if base is None:
                break

            # All elements should match and derived should be longer than base
            if derived != base or derived is None:
                return False

        return True

    def is_base_of(self, other: 'TypeName') -> bool:
        if not isinstance(other, TypeName):
            return False

        return other.is_derived_from(self)
