class ProblemAlreadyExistsError(Exception):
    """Raised when problem with the same title already exists"""

    pass


class ProblemDoesNotExistError(Exception):
    """Raised when someone tries to get a problem by an id that doesn't exist"""

    pass


class OffsetAndLimitMustNotBeNegative(Exception):
    """Raised when offset or limit is not positive or zero"""

    pass
