from typing import Optional
import os


def _truncatestring(s: str, maxlength: Optional[int] = 1000, maxlines: Optional[int] = 20) -> str:
    """
    Helper function to truncate a string to a given length

    :param s: The initial string
    :param maxlength: The amount of characters to truncate at. Takes precedence over maxlines.
    :param maxlines: The amount of lines to truncate at. Lower precedence than maxlength.
    :return: If the string did not exceed either of the limits - the unmodified initial string
             If the string exceeded the length limit - the string truncated to the length limit with
             "...[Truncated]" added to the end
             If the string exceeded the line limit but not the length limit - the string truncated to the
             line limit with "...[Truncated]" added to the end
    """
    if maxlength and len(s) > maxlength:
        return s[0:maxlength - 1] + "...[Truncated]"
    lines = s.splitlines()
    if maxlines and len(lines) > maxlines:
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
            # noinspection IncorrectFormatting
            self.message = "Dumpcs does not appear to be a valid dumpcs:\n" \
                           f"{_truncatestring(content, maxlength=1000, maxlines=20)}"
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
            # noinspection IncorrectFormatting
            self.message = "Dumpcs does not appear to be a valid dumpcs:\n" \
                           f"{_truncatestring(content, maxlength=1000, maxlines=20)}"
        if self.message:
            super().__init__(self.message)
