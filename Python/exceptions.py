class UnexpectedDumpcsFormatError(Exception):
        # Thanks to https://www.programiz.com/python-programming/user-defined-exception
        """Exception raised when a section of dumpcs does not follow a pattern"""

        def __init__(self, message, sample=None, line=None):
            self.message = message
            if sample:
                self.message += f":\n{sample}"
            if line:
                self.message = f"Detected at line {line}: " + self.message
            super().__init__(self.message)


class InvalidDumpcsError(Exception):
    # Thanks to https://www.programiz.com/python-programming/user-defined-exception
    """Exception raised when a section of dumpcs does not follow a pattern"""

    def __init__(self, path):
        self.message = f"Dumpcs file at path {path} is invalid"
        super().__init__(self.message)


def UnexpectedDumpcsFormatWarning(message):
    print(f"UnexpectedDumpcsFormatWarning: {message}")