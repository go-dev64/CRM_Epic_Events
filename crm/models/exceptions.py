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
        return (
            "[prompt.invalid]Invalid password, password must contain:\n"
            "Minimum 8 characters, one should be of Upper Case, special charatere and number between 0-9"
        )


class EmailUniqueError(BaseException):
    """
    Exception class for not unique email error.
    Return error message.
    """

    def __str__(self) -> str:
        return "Email already use!"
