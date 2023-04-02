import os

def truncatestring(s: str, maxlength: int = 1000, maxlines: int = 20) -> str:
    """
    Truncates a string to the given length

    @param s: The initial string
    @param maxlength: The amount of characters to truncate at. Takes precedence over maxlines.
    @param maxlines: The amount of lines to truncate at. Lower precedence than maxlength.
    @return: If the string did not exceed either of the limits - the unmodified initial string
             If the string did exceed either of the limits - the string truncated to the limit with
             "...[Truncated]" added to the end

    Example:
        sub: "string"
        s: "Split this string by delimiter"
        return: " by delimiter"
    """
    if len(s) > maxlength:
        return s[0:maxlength - 1] + "...[Truncated]"
    lines = s.splitlines()
    if len(lines) > maxlines:
        return "\n".join(lines[0:maxlines - 1]) + "...[Truncated]"
    return s

class ValueWarning(Warning):
    pass

class IllegalArgumentException(ValueError):
    pass

class IllegalArgumentWarning(ValueError):
    pass

class UnexpectedDumpcsFormatError(Exception):
    """Exception raised when something unexpected is encountered in a section of dumpcs"""
    def __init__(self, message: str = None, sample: str = None, line: str = None):
        self.message = message if message else ""
        if sample:
            self.message += f":\n{sample}"
        if line:
            self.message = f"Detected at line {line}: " + self.message
        if self.message:
            super().__init__(self.message)

class UnexpectedDumpcsFormatWarning(Warning):
    """Warning raised when something unexpected is encountered in a section of dumpcs"""
    def __init__(self, message: str = None, sample: str = None, line: str = None):
        self.message = message if message else ""
        if sample:
            self.message += f":\n{sample}"
        if line:
            self.message = f"Detected at line {line}: " + self.message
        if self.message:
            super().__init__(self.message)

class InvalidDumpcsError(Exception):
    """Exception raised when a dumpcs in not a valid dumpcs"""
    def __init__(self, path: str | os.PathLike = None, content: str = None):
        """
        Path and content are mutually exclusive, though this is not enforced.
        If both are provided, will default to path
        """
        self.message = None
        if path:
            self.message = f"Dumpcs file at path {path} does not appear to be a valid dumpcs"
        elif content:
            self.message = f"Dumpcs does not appear to be a valid dumpcs:\n{truncatestring(content, maxlength=1000, maxlines=20)}"
        if self.message:
            super().__init__(self.message)

class InvalidDumpcsWarning(Warning):
    """Warning raised when a dumpcs in not a valid dumpcs"""
    def __init__(self, path: str | os.PathLike = None, content: str = None):
        """
        Path and content are mutually exclusive, though this is not enforced.
        If both are provided, will default to path
        """
        self.message = None
        if path:
            self.message = f"Dumpcs file at path {path} does not appear to be a valid dumpcs"
        elif content:
            self.message = f"Dumpcs does not appear to be a valid dumpcs:\n{truncatestring(content, maxlength=1000, maxlines=20)}"
        if self.message:
            super().__init__(self.message)
