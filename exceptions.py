#!/usr/bin/python
# User defined Exceptions


class RetryableException(Exception):
    """
        Super class of all the exceptions which are temporary.
        These can be expected exceptions or dependency exceptions.
    """

    def __init__(self, msg):
        self.msg = msg


class NonRetryableException(Exception):
    """
        Super class of all the exceptions which causes process to stop.
    """

    def __init__(self, msg):
        self.msg = msg


class ValidationException(NonRetryableException):
    """
        Exception raised for errors in input
    Attributes:
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        self.msg = msg


class InvalidEmailFolderException(NonRetryableException):
    """
        Exception raised when Email folder can not be selected
    """

    def __init__(self, msg):
        self.msg = msg


class MessageNotFoundException(RetryableException):
    """
        Exception raised when there is an exception retrieving message(s)
    """

    def __init__(self, msg):
        self.msg = msg


class InvalidCredentials(NonRetryableException):
    """
        Exception raised when invalid credentials are provided
    """

    def __init__(self, msg):
        self.msg = msg


class InvalidSearchCriteria(NonRetryableException):
    """
        Exception raised when invalid credentials are provided
    """

    def __init__(self, msg):
        self.msg = msg
