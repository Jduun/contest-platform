class CredentialsError(Exception):
    """Raised when credentials is wrong"""

    pass


class UsernameAlreadyExistsError(Exception):
    """Raised when user with the same name already exists"""

    pass


class NotEnoughPermissions(Exception):
    """Rased when user has not enough permissions"""

    pass
