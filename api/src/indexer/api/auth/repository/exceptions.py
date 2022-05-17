

class AuthError(Exception):
    pass


class UserNotFound(AuthError):
    pass


class IncorrectCredentials(AuthError):
    pass


class IntegrityError(Exception):
    pass
