class IllegalArgumentException(ValueError):
    pass

class IllegalArgumentWarning(Warning):
    pass


class UnexpectedDumpcsFormatError(Exception):
    # Thanks to https://www.programiz.com/python-programming/user-defined-exception
    """Exception raised when a section of dumpcs does not follow a pattern"""

    def __init__(self, message: str, sample: str = None, line: str = None):
        self.message = message
        if sample:
            self.message += f":\n{sample}"
        if line:
            self.message = f"Detected at line {line}: " + self.message
        super().__init__(self.message)


class InvalidDumpcsError(Exception):
    # Thanks to https://www.programiz.com/python-programming/user-defined-exception
    """Exception raised when a section of dumpcs does not follow a pattern"""

    def __init__(self, path: str):
        self.message = f"Dumpcs file at path {path} is invalid"
        super().__init__(self.message)


class UnexpectedDumpcsFormatWarning(Warning):
    pass
