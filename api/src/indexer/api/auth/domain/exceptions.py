

class AuthError(Exception):
    pass


class UserNotFound(AuthError):
    pass


class DupplicatedUser(AuthError):
    pass


class IncorrectCredentials(AuthError):
    pass


class CredentialsNotFound(AuthError):
    """
    No se encuentran credenciales para permitir procesos de validación.
    """
    pass