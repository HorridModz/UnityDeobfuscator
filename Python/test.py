def readafter(sub: str, s: str, backward=False, regex=False, mustcontain=True, lengthwarning=True) -> str:
    """
    Returns the substring after the delimiter
    If the substring is not found in the string, returns the whole string
    Also supports backward (right to left) and regex

    @param sub: The substring (or regex) to read after
    @param s: The initial string
    @param backward: Whether to read from right to left
    @param regex: Whether to treat the substring as regex
    @param mustcontain: Whether to throw an AssertionError if the substring (or regex) is not present
    in the initial string
    @param lengthwarning: Whether to raise a warning if the substring is longer than the initial string,
    which should never happen (only applies if regex is False)
    @return: The partition of the string after the substring (or regex)

    :raises ImportError: Wrong regex module: Expected regex module, got re module.
    To fix this, replace "import re" with "import regex as re"
    :raises AssertionError: param mustcontain was True and substring (or regex) was not present
    in the initial string
    :warns ValueWarning: param lengthwarning was True, param regex was False, and substring was longer
    than initial string

    Example:
        sub: "string"
        s: "Split this string by delimiter"
        return: " by delimiter"
    """
    class ValueWarning(Warning):
        pass
    # If re isn't imported at all, that will show later.
    # Since we only catch AttributeError, we don't have to worry about it here.
    try:
        re.REVERSE
    except AttributeError:
        raise ImportError("Wrong regex module: Expected regex module, got re module. To fix this, replace \"import "
                          "re\" with \"import regex as re\"")
    if regex:
        sub = f"({sub})"  # Enclose regex with paranthesis to make it a group capture
        if mustcontain:
            assert bool(re.search(sub, s)) is True
        # If an invalid regex is passed, we let re.error throw - it can be handled by the caller
        if backward:
            split = re.split(sub, s, 1, flags=re.REVERSE)
            return split[0]
        else:
            split = re.split(sub, s, 1)
            return split[-1]
    else:
        if lengthwarning and len(sub) > len(s):
            warnings.warn(f"Call to readafter(sub=\"{sub}\", str=\"{s}\"): substring is longer than string",
                          ValueWarning)
        if mustcontain:
            assert sub in s
        if backward:
            prefix, found, suffix = s.rpartition(sub)
        else:
            prefix, found, suffix = s.partition(sub)
        if found:
            return suffix
        else:
            return s

import regex as re
import warnings
readafter("123", "1")