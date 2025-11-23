class BaseAppException(Exception):
    pass


class ValidationException(BaseAppException):
    pass


class DatabaseException(BaseAppException):
    pass
