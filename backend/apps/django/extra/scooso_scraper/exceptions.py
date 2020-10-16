class ConnectionFailed(Exception):
    pass


class LoginFailed(ConnectionFailed):
    pass


class RequestFailed(ConnectionFailed):
    pass


class ParsingFailed(Exception):
    pass


class FileException(Exception):
    pass


class FileManipulatedException(FileException):
    pass
