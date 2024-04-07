from src.location import Location


class IdentifierTooLongError(Exception):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "The identifier you provided is too long."
        self.location = location


class IntegerOverflowError(Exception):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Integer overflow detected."
        self.location = location


class IntegerLeadingZerosError(Exception):
    def __init__(self, location: Location):
        super().__init__(self)
        self.message = "Integer leading zeros detected."
        self.location = location
