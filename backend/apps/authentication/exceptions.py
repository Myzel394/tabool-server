__all__ = [
    "CannotChangeTokenError", "CannotChangeUserError", "UserNotActivatedError"
]


class CannotChangeTokenError(Exception):
    pass


class CannotChangeUserError(Exception):
    pass


class UserNotActivatedError(Exception):
    pass
