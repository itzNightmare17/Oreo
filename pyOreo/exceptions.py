# Oreo - UserBot

"""
Exceptions which can be raised by py-Oreo Itself.
"""

class pyOreoError(Exception):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(pyOreoError):
    ...
