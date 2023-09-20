# Custom class module.


class EmailError(BaseException):
    """
    Exception class for email error.
    Return error message.
    """

    def __str__(self) -> str:
        return "Invalid Email"


class PasswordError(BaseException):
    """
    Exception class for password error.
    Return error message.
    """

    def __str__(self) -> str:
        return "Invalid Password"
