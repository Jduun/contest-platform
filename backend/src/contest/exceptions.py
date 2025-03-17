class ContestDoesNotExistError(Exception):
    """Raised when someone tries to get a contest by an id that doesn't exist"""

    pass


class JoinContestError(Exception):
    """Raised when joining contest is unsuccessfull"""

    pass


class UnjoinContestError(Exception):
    """Raised when unjoining contest is unsuccessfull"""

    pass


class ContestProblemDoesNotExistError(Exception):
    """Raised when someone tries to get a record from ContestProblem by
    an id that doesn't exist"""

    pass


class OffsetAndLimitMustNotBeNegative(Exception):
    """Raised when offset or limit is not positive or zero"""

    pass
