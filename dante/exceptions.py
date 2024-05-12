

"""
Exceptions which can be raised by dante Itself.
"""


class danteError(Exception):
    ...


class TelethonMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(danteError):
    ...
