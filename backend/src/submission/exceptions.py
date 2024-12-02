class SubmissionDoesNotExistError(Exception):
    """Raised when someone tries to get a submission by an id that doesn't exist"""

    pass


class OffsetAndLimitMustNotBeNegative(Exception):
    """Raised when offset or limit is not positive or zero"""

    pass
