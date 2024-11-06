class CredentialsError(Exception):
    """Raised when credentials is wrong"""

    pass


class UsernameAlreadyExistsError(Exception):
    """Raised when user with the same name already exists"""

    pass
