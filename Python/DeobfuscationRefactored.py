"""
TODO: Make everything lazy (only parse objects, methods, params, etc.) when needed

TODO: Make methods able to access other objects and methods (after rewrite):

TODO: Make is standard method detection for methods (Equals, etc.)

TODO: Make is unity type detection

TODO: Replace all terminology with terminology from tools like Il2cppDumper, to make sure it is correct
"""

from __future__ import annotations
import sys
import os
import warnings
import copy
from typing import *
import string
import regex as re
import json
from functools import cache, lru_cache
from typing import Any
# FIXME: Make this a package and make it use relative imports
from unitydeobfuscatorexceptions import *
import fileutils

filehandler = fileutils.FileHandler()


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
            split = re.split(sub, s, 1, )
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



def readbefore(sub: str, s: str, backward=False, regex=False, mustcontain=True, lengthwarning=True) -> str:
    """
    Returns the substring before the delimiter
    If the substring is not found in the string, returns the whole string
    Also supports backward (right to left) and regex

    @param sub: The substring (or regex) to read before
    @param s: The initial string
    @param backward: Whether to read from right to left
    @param regex: Whether to treat the substring as regex
    @param mustcontain: Whether to throw an AssertionError if the substring (or regex) is not present in the initial
    string
    @param lengthwarning: Whether to raise a warning if the substring is longer than the initial string,
    which should never happen (only applies if regex is False)
    @return: The partition of the string before the substring (or regex)

    :raises ImportError: Wrong regex module: Expected regex module, got re module.
    To fix this, replace "import re" with "import regex as re"
    :raises AssertionError: param mustcontain was True and substring (or regex) was not present
    in the initial string
    :warns ValueWarning: param lengthwarning was True, param regex was False, and substring was longer
    than initial string

    Example:
        sub: "string"
        s: "Split this string by delimiter"
        return: "Split this "
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
            return split[-1]
        else:
            split = re.split(sub, s, 1)
            return split[0]
    else:
        if lengthwarning and len(sub) > len(s):
            warnings.warn(f"Call to readbefore(sub=\"{sub}\", str=\"{s}\"): substring is longer than string",
                          ValueWarning)
        if mustcontain:
            assert sub in s
        if backward:
            prefix, found, suffix = s.rpartition(sub)
        else:
            prefix, found, suffix = s.partition(sub)
        if found:
            return prefix
        else:
            return s


def iswhitespace(s: str, totreatblankaswhitespace=True) -> bool:
    """
    Determines if a string is whitespace

    @param s: The string to check
    @param totreatblankaswhitespace: Whether to treat an empty string ("") as whitespace
    @return: Whether the string is whitespace
    """
    if s == "":
        return totreatblankaswhitespace
    else:
        return s.isspace()


def trim(s: str, leading=True, trailing=True) -> str:
    """
    Trims whitespace from a string

    @param s: The initial string
    @param leading: Whether to trim leading whitespace
    @param trailing: Whether to trim trailing whitespace
    @return: String with whitespace trimmed

    Example:
        s: "   hello world!
        "
        leading: True
        trailing: True
        return: "hello world!"
    """
    if leading and trailing:
        return s.strip()
    elif leading:
        return s.lstrip()
    elif trailing:
        return s.rstrip()
    else:
        return s


# FIXME: Why does caching this cause bugs?
#@cache
def getwords(s: str, customregex=None) -> list[str]:
    """
    Splits a string into a list of words
    Treats any whitespace as a word delimiter, including newlines and tabs
    If a chunk of whitespace is encountered (ex: "\t\n" or "  ", the whole thing
    will be considered one delimiter

    @param s: The string to split into words
    @param customregex: Instead of using built-in strng.split method, split by custom regex
    @return: List of words in the initial string (in order)

    Example:
        s: "the quick
                    brown       fox

                 abcdefg  "
        return: ["the","quick","brown","fox","abcdefg"]
    """
    if customregex:
        return re.split(customregex, s)
    else:
        return s.split()


def wordstostring(words: list[str],
                  totrimwords=False,
                  toignoreblankwords=False,
                  concatenator=" ") -> str:
    """
    Joins a list of words into a string

    @param words: The list of words to concatenate
    @param totrimwords: Whether to trim whitespace from words. Trims both leading and trailing whitespace.
    @param toignoreblankwords: Whether to ignore words that are only whitespace
    @param concatenator: Delimiter to concatenate words with (default " ")
    @return: Words concatenated by concatenator
    """
    wordstoconcatenate = []
    for word in words:
        if iswhitespace(word) and toignoreblankwords:
            continue
        if totrimwords:
            word = trim(word, True, True)
        wordstoconcatenate.append(word)
    return concatenator.join(wordstoconcatenate)


def getlines(s: str,
             toremoveblanklines=False,
             totrimlines=False) -> list[str]:

    """
    Splits a string into a list of lines

    @param s: The string to split into lines
    @param toremoveblanklines: Whether to ignore lines that are blank or only whitespace
    @param totrimlines: Wwhether to trim whitespace from each line (leading and trailing)
    @return: List of lines in the string (in order)

    Example:
        s "a

                    b

                 c  "
        toremoveblanklines: True
        totrimlines: True
        return: ["a","b","c"]
    """
    lines = s.splitlines()
    newlines = []
    for line in lines:
        if totrimlines:
            line = trim(line, True, True)
        if not (toremoveblanklines and iswhitespace(line)):
            newlines.append(line)
    return newlines
    # return [trim(line, True, True) if totrimlines else line
    #         for line in s.splitlines()
    #         if not (toremoveblanklines and iswhitespace(line))]


def linestostring(lines: list[str],
                  totrimlines=False,
                  toignoreblanklines=False,
                  concatenator="\n") -> str:
    """
    Joins a list of lines into a string

    @param lines: The list of lines to concatenate
    @param totrimlines: Whether to trim whitespace from lines. Trims both leading and trailing whitespace.
    @param toignoreblanklines: Whether to ignore lines that are only whitespace
    @param concatenator: Delimiter to concatenate lines with (default "\n")
    @return: Lines concatenated by concatenator

    Example:
        lines: ["a","","b","    ","cd",""]
        toignoreblanklines: False
        totrimlines: False
        Return: "a

                 b

                 cd
                 "
    """
    # This function is exactly the same as wordstostring, except it operates on lines and
    # "\n" is the default concatenator. So, it's best to reuse the wordstostring function here.
    return wordstostring(lines, totrimlines, toignoreblanklines, concatenator)


@cache
def datatype_isreference(datatype: str) -> bool:
    # Not Done
    words = getwords(datatype, customregex="(?<!,) ")
    assert len(words) > 1
    return "ref" in words


def dumpcs_isvalid(dumpcs: str) -> bool:
    # Not done
    """

    Determines whether a dumpcs file is valid
    Works by checking against some substrings that some should exist in all valid dump.cs files
    All dumpcs files entered should be valid, but of course they must be checked.
    Note: This function only performs a short check on the file as a whole.
    On the other hand, the dumpcs_checkformat function analyzes the whole thing and is very picky.

    Arguments:
        dumpcs: the raw content of the dumpcs file

    Return:
        whether the dumpcs is valid
    """
    checks = ("// Image 0:", "// Namespace: ", "class", "\n\t// Methods", "// RVA: 0x")
    for check in checks:
        if check not in dumpcs:
            return False
    return True


def dumpcs_checkformat(dumpcs: str) -> list[dict]:
    # Not Done
    """
    Scan dump.cs for unexpected formatting
    Returns list of unexpected formatting errors

    Arguments:
        dumpcs: the raw content of the dumpcs file

    Return:
        list of errors with the line number and error message
    """
    raise NotImplementedError("Dumpcs_checkformat function not completed")


def dumpcs_hasattributes(dumpcs: str, fastcheck=False) -> bool:
    # Done
    """

    Possible Improvements:
        1. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity

    Determines whether a dumpcs file has attributes

    Arguments:
        dumpcs: the raw content of the dumpcs file
        fastcheck: whether to perform a fast or thorough check for attributes (fast should be sufficient,
        but it is safer to perform a thorough check)

    Return:
        whether the dumpcs file has attributes
    """
    if fastcheck:
        return "[CompilerGeneratedAttribute]" in dumpcs
    else:
        lines = getlines(dumpcs, False, False)
        for line in lines:
            # Trim leading whitespace from line
            trimmedline = trim(line, True, False)
            # If the first non-whitespace character on the line is a square bracket,
            # this means the line is an attribute
            if trimmedline and trimmedline[0] == "[":
                return True
        return False


def dumpcs_constructor(dumpcs: str, terminateifinvalid: True) -> list[list[dict]]:
    # Done
    """
    Possible Improvements:
        1. Setting dumpcs variable after removing attributes makes code more readable and concise,
        but is less inefficient than directing passing result of dumpcs_removeattributes.
        In addition, attributes must be removed before dumpcs is checked for format errors
        2. Directly using dumpcs_removeattributes instead of checking with dumpcs_hasattributes may be faster
        (idk if it is), but it sacrifices readability

    Loads and initializes a dumpcs
    Checks validity of the dumpcs and searches for format errors
    Parser images and objects in dumpcs
    (Sets fields for images and objects)

    Arguments:
        dumpcs: the raw content of the dumpcs file
        terminateifinvalid: whether to terminate with an error or just throw a warning
        if the dumpcs appears to be invalid

    Return:
        List of objects in the dumpcs file

    :raises InvalidDumpcsError: The dumpcs appears to be invalid, and terminateifinvalid was True
    :warns InvalidDumpcsWarning: The dumpcs appears to be invalid, and terminateifinvalid was False
    """
    if not dumpcs_isvalid(dumpcs):
        if terminateifinvalid:
            raise InvalidDumpcsError(content=dumpcs)
        else:
            warnings.warn(InvalidDumpcsWarning(content=dumpcs))
    if dumpcs_hasattributes(dumpcs):
        dumpcs = dumpcs_removeattributes(dumpcs)
    formaterrors = dumpcs_checkformat(dumpcs)
    if formaterrors:
        for formaterror in formaterrors:
            raise UnexpectedDumpcsFormatError(formaterror.message, formaterror.sample, line=formaterror.line)
    images = dumpcs_getimages(dumpcs)
    objects = dumpcs_getobjects(dumpcs)
    return objects


def dumpcs_removeattributes(dumpcs: str) -> str:
    # Done
    """
    Possible Improvements:
        1. Creating a new list of lines is inefficient, modifying existing list would be ideal
        2. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity

    Removes attributes from a dumpcs file
    Does not process attributes, only removes them
    Does not remove blank lines

    Arguments:
        dumpcs: the raw content of the dumpcs file

    Return:
        dumpcs raw content with attributes removed
   """
    lines = getlines(dumpcs, False, False)
    newlines = []
    for line in lines:
        # Trim leading whitespace from line
        trimmedline = trim(line, True, False)
        # If the first non-whitespace character on the line is a square bracket,
        # this means the line is an attribute
        if trimmedline == "" or trimmedline[0] != "[":
            # The line is not an attribute line, so keep it
            newlines.append(line)
    return linestostring(newlines, False, False)


@cache
def dumpcsobject_hasnamespace(rawobject: str) -> bool:
    # Not Done
    lines = getlines(rawobject)
    namespaceline = lines[0]
    return namespaceline != "// Namespace: "


@cache
def dumpcsobject_getnamespace(rawobject: str) -> Optional[str]:
    # Done
    """

    Possible Improvements:

    Gets the namespace of a dumpcs object

    Example:
        namespaceline: // Namespace: Microsoft.Win32
        Return: Microsoft.Win32


    Arguments:
        rawobject: the raw content of the dumpcs object

    Return:
        namespace of the dumpcs sobject
    """
    if not dumpcsobject_hasnamespace(rawobject):
        # No namespace
        return None
    lines = getlines(rawobject)
    namespaceline = lines[0]
    # Everything after "// Namespace: " in the namespaceline is the object's namespace
    namespacedelimiter = "// Namespace: "
    namespace = readafter(namespacedelimiter, namespaceline)
    return namespace


@cache
def dumpcsobject__getmodifiers(rawobject: str) -> list[str]:
    # Done
    """

    Possible Improvements:
        1.  Directly returning instead of using type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        2. Object types should be a constant
        3. IDK if using a dictionary cache is faster or ironically slower

    Gets the type (struct, class, enum, or interface) of a dumpcs object

    Example:
        objectsignatureline: public static class Registry // TypeDefIndex: 4
        Return: class


    Arguments:
        rawobject: the raw content of the dumpcs object

    Return:
        type of the dumpcs object
    """
    lines = getlines(rawobject)
    objectsignatureline = lines[1].strip()
    if dumpcsobject_isinherited(rawobject):
        # If the object is inherited, read before the base class (to get the derived class)
        prefix = readbefore(" : ", objectsignatureline)
    else:
        # If the object is not inherited, read before the typedefindex
        prefix = readbefore(" //", objectsignatureline)
    words = getwords(prefix, customregex="(?<!,) ")  # This regex will match " " unless it is prefixed by ","
    assert len(words) > 1
    # Last word is object name, second to last word is object type
    del words[-1:-2]
    while words[-1] in "ref, in, out":
        datatype += f"{words[-3]} "
        del words[-3]
    return words


@cache
def dumpcsobject_getobjecttype(rawobject: str) -> str:
    # Done
    """

    Possible Improvements:
        1.  Directly returning instead of using type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        2. Object types should be a constant
        3. IDK if using a dictionary cache is faster or ironically slower

    Gets the type (struct, class, enum, or interface) of a dumpcs object

    Example:
        objectsignatureline: public static class Registry // TypeDefIndex: 4
        Return: class


    Arguments:
        rawobject: the raw content of the dumpcs object

    Return:
        type of the dumpcs object
    """
    lines = getlines(rawobject)
    objectsignatureline = lines[1].strip()
    if dumpcsobject_isinherited(rawobject):
        # If the object is inherited, read before the base class (to get the derived class)
        prefix = readbefore(" : ", objectsignatureline)
    else:
        # If the object is not inherited, read before the typedefindex
        prefix = readbefore(" //", objectsignatureline)
    words = getwords(prefix, customregex="(?<!,) ")  # This regex will match " " unless it is prefixed by ","
    assert len(words) > 1
    # Last word is object name, second to last word is object type
    objecttype = words[-2]
    return objecttype


@cache
def dumpcsobject_getdatatype(rawobject: str) -> str:
    # Done
    """

    Possible Improvements:
        1.  Directly returning instead of using type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        2. Using a string for data type instead of using a list and concatenating it into a string may be faster,
        but sacrifices readability and simplicity
        3. Object types should be a constant
        4. IDK if using a dictionary cache is faster or ironically slower

    Gets the data type of a dumpcs object

    Example:
        objectsignatureline: public static class Registry // TypeDefIndex: 4
        Return: public static


    Arguments:
        rawobject: the raw content of the dumpcs object

    Return:
        data type of the dumpcs object
    """
    lines = getlines(rawobject)
    objectsignatureline = lines[1].strip()
    if dumpcsobject_isinherited(rawobject):
        # If the object is inherited, read before the base class (to get the derived class)
        prefix = readbefore(" : ", objectsignatureline)
    else:
        # If the object is not inherited, read before the typedefindex
        prefix = readbefore(" //", objectsignatureline)
    words = getwords(prefix, customregex="(?<!,) ")  # This regex will match " " unless it is prefixed by ","
    assert len(words) > 1
    # Delete object name and object type
    del words[-1:-2]
    datatype = wordstostring(words)
    return datatype


@cache
def dumpcsobject_getname(rawobject: str, includenesting=False) -> str:
    # Done
    """

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets the name of a dumpcs object

    Examples:
        objectsignatureline: private enum SimpleCollator.ExtenderType // TypeDefIndex: 41
        includenesting: True
        Return: SimpleCollator.ExtenderType

        objectsignatureline: private enum SimpleCollator.ExtenderType // TypeDefIndex: 41
        includenesting: False
        Return: ExtenderType


    Arguments:
        rawobject: the raw content of the dumpcs object
        includenesting: whether to include the outer objects in the name
        (only applies if the object is nested)

    Return:
        the name of the dumpcs object
    """
    lines = getlines(rawobject)
    objectsignatureline = lines[1].strip()
    if dumpcsobject_isinherited(rawobject):
        # If the object is inherited, read before the base class (to get the derived class)
        prefix = readbefore(" : ", objectsignatureline)
    else:
        # If the object is not inherited, read before the typedefindex
        prefix = readbefore(" //", objectsignatureline)
    if dumpcsobject_isgeneric(rawobject):
        # Match generics, but not compiler generated symbols
        # EX: IEnumerator<object>, but not TweenRunner.<Start>
        prefix = readbefore("(?!^)(?<!\.)<(?!>)", prefix, regex=True)
    # The name of the object is the last word before the delimiter in the objectsignatureline
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    fullname = words[-1] #including nesting (if any)
    if includenesting:
        name = fullname
    else:
        nesting = fullname.split(".")
        # Last element is the name of the object (without nesting, if any)
        name = nesting[-1]
    return name


@cache
def dumpcsobject_getbases(rawobject: str) -> list[str]:
    # Not Done
    """
    Docs Not Done!

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets the base class of a dumpcs object
    If the object is not inherited, returns None

    Examples:
        objectsignatureline: public static class Registry // TypeDefIndex: 4
        Return: None

        objectsignatureline: public class DecalsMeshRenderer : MonoBehaviour // TypeDefIndex: 4727
        Return: MonoBehavior


    Arguments:
        rawobject: the raw content of the dumpcs object

    Returns:
        base class of the dumpcs object, or None if the dumpcs object is not inherited
    """
    lines = getlines(rawobject)
    objectsignatureline = lines[1].strip()
    if not dumpcsobject_isinherited(rawobject):
        return None
    suffix = readafter(" : ", objectsignatureline)
    basessection = readbefore(" //", suffix)
    # Split basessection by ", ", which can be used to mark the start of each base
    # Make sure not to split by ", " in data types (such as Dict<string, int>)
    rawbases = []
    thisbase = ""
    previousletter = None
    datatypelayer = 0
    iterable = iter(basessection)
    for letter in iterable:
        # This code will treat compiler generated symbols (such as .<Start>) as generics
        # This is unintentional, but it doesn't matter in this case
        if datatypelayer >= 1 and letter == ">":
            datatypelayer -= 1
        elif letter == "<":
            datatypelayer += 1
        elif datatypelayer == 0 and letter == ",":
            # Call next() on iterator to skip the character after this one (space)
            rawbases.append(thisbase)
            thisbase = ""
            next(iterable)
            # Continue to skip this letter (","), so it does not get added to this param
            continue
        thisbase += letter
        previousletter = letter
    if thisbase != "":
        # Add last base (it did not get added because there is no comma after it)
        rawbases.append(thisbase)
    if not rawbases:
        return []
    # Build dictionary of bases from raw bases
    bases = []
    for rawbase in rawbases:
        name = dumpcsobject_base_getname(rawbase)
        isgeneric = dumpcsobject_base_isgeneric(rawbase)
        genericdatatype = dumpcsobject_base_getgenericdatatype(rawbase) if isgeneric else None
        base = {
            "raw": rawbase,
            "name": name,
            "isgeneric": isgeneric,
            "genericdatatype": genericdatatype,
        }
        bases.append(base)
    return bases

@cache
def dumpcsobject_base_getname(rawbase: str) -> str:
    if dumpcsobject_base_isgeneric(rawbase):
        # Match generics, but not compiler generated symbols
        # EX: IEnumerator<object>, but not TweenRunner.<Start>
        return readbefore("(?!^)(?<!\.)<(?!>)", rawbase, regex=True)
    else:
        return rawbase

@cache
def dumpcsobject_base_isgeneric(rawbase: str) -> bool:
    # Not Done
    # Match generics, but not compiler generated symbols
    # EX: IEnumerator<object>, but not TweenRunner.<Start>
    if re.search("(?!^)(?!^)(?<!\.)<(?!>)", rawbase):
        return True
    else:
        return False


@cache
def dumpcsobject_base_getgenericdatatype(rawbase: str) -> str:
    # Not Done
    if not dumpcsobject_base_isgeneric(rawbase):
        # Not generic
        return None
    # Match generics, but not compiler generated symbols
    # EX: IEnumerator<object>, but not TweenRunner.<Start>
    suffix = readafter("(?!^)(?<!\.)<(?!>)", rawbase, regex=True)
    genericdatatype = readbefore("(?<!\<)>", suffix, regex=True, backward=True)
    return genericdatatype

@cache
def dumpcsobject_isabstract(rawobject: str) -> bool:
    # Not Done
    if dumpcsobject_getobjecttype(rawobject) == "interface":
        # Interfaces are implicity abstract
        return True
    modifiers = dumpcsobject__getmodifiers(rawobject)
    return "abstract" in modifiers

@cache
def dumpcsobject_isstatic(rawobject: str) -> bool:
    # Not Done
    modifiers = dumpcsobject__getmodifiers(rawobject)
    return "static" in modifiers

@cache
def dumpcsobject_issealed(rawobject: str) -> bool:
    # Not Done
    modifiers = dumpcsobject__getmodifiers(rawobject)
    return "sealed" in modifiers


@cache
def dumpcsobject_getnesting(rawobject: str, includename=False, innertoouter=True) -> tuple:
    # Not Done
    # Ex: a.b.c -> (c, b, a)
    fullname = dumpcsobject_getname(rawobject, includenesting=True) # including nesting (if any)
    nesting = fullname.split(".")
    if not includename:
        # Remove last element as this is the name of the object (without nesting, if any)
        del nesting[-1]
    if innertoouter:
        # Reverse the list to make the order go from inner to outer rather than outer to inner
        nesting.reverse()
    return tuple(nesting)


@cache
def dumpcsobject_isnested(rawobject: str) -> bool:
    nesting = dumpcsobject_getnesting(rawobject)
    if nesting:
        return True
    else:
        return False


@cache
def dumpcsobject_getpath(rawobject: str) -> str:
    hasnamespace = dumpcsobject_hasnamespace(rawobject)
    namespace = dumpcsobject_getnamespace(rawobject)
    name = dumpcsobject_getname(rawobject)
    nesting = dumpcsobject_getnesting(rawobject, includename=False, innertoouter=False)
    path = ""
    if hasnamespace:
        path += f"{namespace}::"
    for nestinglevel in nesting:
        path += f"{nestinglevel}."
    path += name
    return path


@cache
def dumpcsobject_isgeneric(rawobject: str) -> bool:
    # Not Done
    lines = getlines(rawobject)
    objectsignatureline = lines[1].strip()
    if dumpcsobject_isinherited(rawobject):
        # If the object is inherited, read before the base class (to get the derived class)
        prefix = readbefore(" : ", objectsignatureline)
    else:
        # If the object is not inherited, read before the typedefindex
        prefix = readbefore(" //", objectsignatureline)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    lastword = words[-1]
    # Match generics, but not compiler generated symbols
    # EX: IEnumerator<object>, but not TweenRunner.<Start>
    if re.search("(?!^)(?<!\.)<(?!>)", lastword):
        return True
    else:
        return False


@cache
def dumpcsobject_getgenerictypename(rawobject: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_isgeneric(rawobject):
        # Not generic
        return None
    lines = getlines(rawobject)
    objectsignatureline = lines[1].strip()
    if dumpcsobject_isinherited(rawobject):
        # If the object is inherited, read before the base class (to get the derived class)
        prefix = readbefore(" : ", objectsignatureline)
    else:
        # If the object is not inherited, read before the typedefindex
        prefix = readbefore(" //", objectsignatureline)
    # Match generics, but not compiler generated symbols
    # EX: IEnumerator<object>, but not TweenRunner.<Start>
    suffix = readafter("(?!^)(?<!\.)<(?!>)", prefix, regex=True)
    generictypename = readbefore("(?<!\<)>", suffix, regex=True, backward=True)
    return generictypename


@cache
def dumpcsobject_gettypedefindex(rawobject: str) -> str:
    # Done
    """

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets the typedefindex of a dumpcs object

    Example:
        objectsignatureline: public static class Registry // TypeDefIndex: 4
        Return: 4

    Arguments:
        rawobject: the raw content of the dumpcs object

    Return:
        typedefindex of the dumpcs object
    """
    lines = getlines(rawobject)
    objectsignatureline = lines[1].strip()
    typedefindex = readafter("// TypeDefIndex: ", objectsignatureline)
    return typedefindex


@cache
def dumpcsobject_isinherited(rawobject: str) -> bool:
    # Done
    """

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Determines whether a dumpcs object is inherited

    Examples:
        objectsignatureline: public static class Registry // TypeDefIndex: 4
        Return: False

        objectsignatureline: public class DecalsMeshRenderer : MonoBehaviour // TypeDefIndex: 4727
        Return: True

    Arguments:
        rawobject: the raw content of the dumpcs object

    Return:
        whether the dumpcs object is inherited
    """
    lines = getlines(rawobject)
    objectsignatureline = lines[1].strip()
    return " : " in objectsignatureline


@cache
def dumpcsobject__hasmethods(rawobject: str) -> bool:
    return "\n\t// Methods" in rawobject


@cache
def dumpcsobject__hasfields(rawobject: str) -> bool:
    return "\n\t// Fields" in rawobject


@cache
def dumpcsobject__hasproperties(rawobject: str) -> bool:
    return "\n\t// Properties" in rawobject


@cache
def dumpcsobject_getmethods(rawobject: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of methods from a dumpcs object
    Includes list of generics in each method

    rawobject: the raw content of the dumpcs object

    Return:
        list of methods in the dumpcs object
    """
    # Get the methods section of the dumpcs object
    if not dumpcsobject__hasmethods(rawobject):
        # No Methods
        return []
    suffix = readafter("\n\t// Methods", rawobject)
    checks = ("\n\t// Fields", "\n\t// Properties")
    found = False
    for check in checks:
        if check in suffix:
            methodssection = readbefore(f"\n{check}", suffix)
            found = True
            break
    if not found:
        methodssection = readbefore("\n}", suffix, backward=True)
    methoddelimiter = "\n\n"
    # Split methodssection by "\n\n", which can be used to mark the start of each method
    rawmethods = methodssection.split(methoddelimiter)
    if not rawmethods:
        return []
    # The split function will capture everything before the first method
    # since we split by the delimiter that starts methods, so delete that
    del rawmethods[0]
    # Build dictionary of methods from raw methods
    methods = []
    for rawmethod in rawmethods:
        isconstructor = dumpcsobject_method_isconstructor(rawmethod)
        isstaticconstructor = dumpcsobject_method_isstaticconstructor(rawmethod)
        isdestructor = dumpcsobject_method_isdestructor(rawmethod)
        isoperator = dumpcsobject_method_isoperator(rawmethod)
        isupdate = dumpcsobject_method_isupdate(rawmethod)
        updatetype = dumpcsobject_method_getupdatetype(rawmethod) if isupdate else None
        if isconstructor or isstaticconstructor:
            name = dumpcsobject_getname(rawobject, includenesting=False)
        elif isdestructor:
            name = f"~{dumpcsobject_getname(rawobject, includenesting=False)}"
        else:
            name = dumpcsobject_method_getname(rawmethod)
        datatype = dumpcsobject_method_getdatatype(rawmethod)
        visibility = dumpcsobject_method_getvisibility(rawmethod)
        isvoid = dumpcsobject_method_isvoid(rawmethod)
        isoverride = dumpcsobject_method_isoverride(rawmethod)
        isvirtual = dumpcsobject_method_isvirtual(rawmethod)
        # We don't have to check if the object is static, but this is a shortcut
        isstatic = True if dumpcsobject_isstatic(rawobject) else dumpcsobject_method_isstatic(rawmethod)
        # This is an example of where methods being able to access other objects and methods would be useful
        # - so we could put this in the dumcsobject_method_isabstract function instead of having to check
        # for it here
        isabstract = True if dumpcsobject_isabstract(rawobject) else dumpcsobject_method_isabstract(rawmethod)
        isextern = dumpcsobject_method_isextern(rawmethod)
        hasslot = dumpcsobject_method_hasslot(rawmethod)
        slot = dumpcsobject_method_getslot(rawmethod) if hasslot else None
        isgenericinstmethod = dumpcsobject_method_isgenericinstmethod(rawmethod)
        generics = dumpcsobject_method_getgenerics(rawmethod) if isgenericinstmethod else []
        isgeneric = dumpcsobject_method_isgeneric(rawmethod)
        generictypename = dumpcsobject_method_getgenerictypename(rawmethod) if isgeneric else None
        hasoffsetdata = dumpcsobject_method_hasoffsetdata(rawmethod) # Offset -1 if not
        if hasoffsetdata:
            relativevirtualaddress = dumpcsobject_method_getrelativevirtualaddress(rawmethod) #RVA
            virtualaddress = dumpcsobject_method_getvirtualaddress(rawmethod) #VA
            offset = dumpcsobject_method_getoffset(rawmethod) #Offset
        else:
            relativevirtualaddress = None  # RVA
            virtualaddress = None  # VA
            offset = None  # Offset
        params = dumpcsobject_method_getparams(rawmethod)
        method = {
            "raw": rawmethod,
            "name": name,
            "isconstructor": isconstructor,
            "isstaticconstructor": isstaticconstructor,
            "isoperator": isoperator,
            "isupdate": isupdate,
            "updatetype": updatetype,
            "datatype": datatype,
            "isvoid": isvoid,
            "isvirtual": isvirtual,
            "isoverride": isoverride,
            "isabstract": isabstract,
            "isstatic": isstatic,
            "isextern": isextern,
            "hasslot": hasslot,
            "slot": slot,
            "hasoffsetdata": hasoffsetdata,
            "relativevirtualaddress": relativevirtualaddress,
            "offset": offset,
            "virtualaddress": virtualaddress,
            "params": params,
            "isgenericinstmethod": isgenericinstmethod,
            "generics": generics,
            "isgeneric": isgeneric,
            "generictypename": generictypename,
                }
        methods.append(method)
    return methods


@cache
def dumpcsobject_method_getname(rawmethod: str) -> str:
    # Not Done
    lines = getlines(rawmethod)
    methodsignatureline = lines[1].strip()
    prefix = readbefore("(", methodsignatureline)
    # TODO: Split everything like this (every signature) with words = re.split("(?<!,) ", objecttype)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # The name of the method is the last word before the delimiter in the methodsignatureline
    lastword = words[-1]
    if dumpcsobject_method_isgeneric(rawmethod):
        # Match generics, but not compiler generated symbols
        # EX: IEnumerator<object>, but not TweenRunner.<Start>
        prefix = readbefore("(?!^)(?<!\.)<(?!>)", lastword, regex=True)
        suffix = readafter("(?<!\<)>", lastword, regex=True, backward=True)
        name = prefix + suffix
    else:
        name = lastword
    return name


@cache
def dumpcsobject_method_isconstructor(rawmethod: str) -> bool:
    # Not Done
    # We don't need to check if the method is static, because the name tells us
    name = dumpcsobject_method_getname(rawmethod)
    return name == ".ctor"


@cache
def dumpcsobject_method_isstaticconstructor(rawmethod: str) -> bool:
    # Not Done
    # We don't need to check if the method is static, because the name tells us
    name = dumpcsobject_method_getname(rawmethod)
    return name == ".cctor"

@cache
def dumpcsobject_method_isdestructor(rawmethod: str) -> bool:
    # Not Done
    name = dumpcsobject_method_getname(rawmethod)
    return name == "Finalize"


@cache
def dumpcsobject_method_isoperator(rawmethod: str) -> bool:
    # Not Done
    """
    WARNING:
    Overloaded operators are not actually represented as operators in compiled unity games
    The only way to tell if they are operators is if they use the operator naming convention,
    which is automatically generated by the Il2CPP compiler. This naming convention is to
    prefix them with "op_", then put the name of the operator (ex: op_Addition).
    However, it is possible for a programmer or obfuscator to use this naming convention in their
    own methods. This would be bad practice, but it would be practical for obfuscation. If this is done,
    it will cause this function to give false positives about methods being operators.
    In addition, the opposite is true: Technically, the overloaded operators don't have to start with op_,
    and after compilation, their names can be changed.
    """
    name = dumpcsobject_method_getname(rawmethod)
    return name.startswith("op_")


@cache
def dumpcsobject_method_isupdate(rawmethod: str) -> bool:
    # Not Done
    name = dumpcsobject_method_getname(rawmethod)
    UPDATENAMES = {"FixedUpdate", "LateUpdate", "Update"} # Should be a constant!
    return name in UPDATENAMES


@cache
def dumpcsobject_method_getupdatetype(rawmethod: str) -> str:
    # Not Done
    if dumpcsobject_method_isupdate(rawmethod):
        name = dumpcsobject_method_getname(rawmethod)
        UPDATENAMES = {"FixedUpdate", "LateUpdate", "Update"}  # Should be a constant!
        assert name in UPDATENAMES
        return name
    else:
        # No update type
        return None


@cache
def dumpcsobject_method_isgeneric(rawmethod: str) -> str:
    # Not Done
    lines = getlines(rawmethod)
    methodsignatureline = lines[1].strip()
    prefix = readbefore("(", methodsignatureline)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    lastword = words[-1]
    # Match generics, but not compiler generated symbols
    # EX: IEnumerator<object>, but not TweenRunner.<Start>
    if re.search("(?!^)(?<!\.)<(?!>)", lastword):
        return True
    else:
        return False

@cache
def dumpcsobject_method_getgenerictypename(rawmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_isgeneric(rawmethod):
        # No generic type
        return None
    lines = getlines(rawmethod)
    methodsignatureline = lines[1].strip()
    prefix = readbefore("(", methodsignatureline)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # The name of the method is the last word before the delimiter in the methodsignatureline
    name = words[-1]
    suffix = readafter("<", name)
    generictype = readbefore(">", suffix, backward=True)
    return generictype


@cache
def dumpcsobject_method_getvisibility(rawmethod: str) -> str:
    # Not Done
    lines = getlines(rawmethod)
    methodsignatureline = lines[1].strip()
    prefix = readbefore("(", methodsignatureline)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # Delete method name
    del words[-1]
    ACCESSMODIFIERS = {"public", "private", "protected", "internal"}  # should be a constant!
    # visibilitywords = []
    # for word in words:
    #     if word not in ACCESSMODIFIERS:
    #         break
    #     # Add this word onto the visibility
    #     visibilitywords.append(word)
    # # Concatenate the words back into a string
    # visibility = wordstostring(visibilitywords)
    visibility = wordstostring([word for word in words if word in ACCESSMODIFIERS])
    return visibility


@cache
def dumpcsobject_method__getmodifiers(rawmethod: str) -> list[str]:
    # Not Done
    lines = getlines(rawmethod)
    methodsignatureline = lines[1].strip()
    prefix = readbefore("(", methodsignatureline)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # Delete method name
    del words[-1]
    ACCESSMODIFIERS = {"public", "private", "protected", "internal"}  # should be a constant!
    modifiers = [word for word in words if word not in ACCESSMODIFIERS]
    return modifiers


@cache
def dumpcsobject_method_getdatatype(rawmethod: str) -> str:
    # Not Done
    lines = getlines(rawmethod)
    methodsignatureline = lines[1].strip()
    prefix = readbefore("(", methodsignatureline)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # Last word is method name
    del words[-1]
    # The data type is always one word, except for references
    # (such as ref int)
    if words[-2] == "ref":
        datatype = words[-2:-1]
    else:
        datatype = words[-1]
    return datatype


@cache
def dumpcsobject_method_isvoid(rawmethod: str) -> bool:
    # Not Done
    datatype = dumpcsobject_method_getdatatype(rawmethod)
    return datatype == "void"


@cache
def dumpcsobject_method_isvirtual(rawmethod: str) -> bool:
    # Not Done
    modifiers = dumpcsobject_method__getmodifiers(rawmethod)
    return "virtual" in modifiers

@cache
def dumpcsobject_method_isabstract(rawmethod: str) -> bool:
    # Not Done
    modifiers = dumpcsobject_method__getmodifiers(rawmethod)
    return "abstract" in modifiers

@cache
def dumpcsobject_method_isstatic(rawmethod: str) -> bool:
    # Not Done
    modifiers = dumpcsobject_method__getmodifiers(rawmethod)
    return "static" in modifiers


@cache
def dumpcsobject_method_isoverride(rawmethod: str) -> bool:
    # Not Done
    # Note: Override keyword is *required* to override, even for abstract methods and classes,
    # making our life much easier.
    # TODO: Also check if base method is virtual
    modifiers = dumpcsobject_method__getmodifiers(rawmethod)
    return "override" in modifiers


@cache
def dumpcsobject_method_isextern(rawmethod: str) -> bool:
    # Not Done
    modifiers = dumpcsobject_method__getmodifiers(rawmethod)
    return "extern" in modifiers


@cache
def dumpcsobject_method_hasslot(rawmethod: str) -> bool:
    # Not Done
    lines = getlines(rawmethod)
    offsetdataline = lines[0]
    offsetdataline = offsetdataline.strip()
    return "Slot: " in offsetdataline


@cache
def dumpcsobject_method_getslot(rawmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_hasslot(rawmethod):
        # No slot
        return None
    lines = getlines(rawmethod)
    offsetdataline = lines[0].strip()
    suffix = readafter("Slot: ", offsetdataline)
    # if " " in suffix:
    #     slot = readbefore(" ", suffix)
    # else:
    #     slot = suffix
    slot = readbefore(" ", suffix, mustcontain=False)
    return slot

@cache
def dumpcsobject_method_isgenericinstmethod(rawmethod: str) -> bool:
    # Not Done
    return "\t/* GenericInstMethod :" in rawmethod


@cache
def dumpcsobject_method_hasoffsetdata(rawmethod: str) -> bool:
    # Not Done
    lines = getlines(rawmethod)
    offsetdataline = lines[0].strip()
    if  "Offset: " not in offsetdataline:
        return False
    if "Offset: -1" in offsetdataline:
        hasoffsetdata = False
    else:
        hasoffsetdata = True
    if hasoffsetdata:
        assert "RVA: " in offsetdataline
        assert "VA: " in offsetdataline
    return hasoffsetdata


@cache
def dumpcsobject_method_getrelativevirtualaddress(rawmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_hasoffsetdata(rawmethod):
        return None
    lines = getlines(rawmethod)
    offsetdataline = lines[0].strip()
    suffix = readafter("RVA: ", offsetdataline)
    # if " " in suffix:
    #     relativevirtualaddress = readbefore(" ", suffix)
    # else:
    #     relativevirtualaddress = suffix
    relativevirtualaddress = readbefore(" ", suffix, mustcontain=False)
    return relativevirtualaddress


@cache
def dumpcsobject_method_getoffset(rawmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_hasoffsetdata(rawmethod):
        return None
    lines = getlines(rawmethod)
    offsetdataline = lines[0].strip()
    suffix = readafter("Offset: ", offsetdataline)
    # if " " in suffix:
    #     offset = readbefore(" ", suffix)
    # else:
    #     offset = suffix
    offset = readbefore(" ", suffix, mustcontain=False)
    return offset


@cache
def dumpcsobject_method_getvirtualaddress(rawmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_hasoffsetdata(rawmethod):
        return None
    lines = getlines(rawmethod)
    offsetdataline = lines[0].strip()
    suffix = readafter("VA: ", offsetdataline)
    # if " " in suffix:
    #     virtualaddress = readbefore(" ", suffix)
    # else:
    #     virtualaddress = suffix
    virtualaddress = readbefore(" ", suffix, mustcontain=False)
    return virtualaddress


@cache
def dumpcsobject_method_getgenerics(rawmethod: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of generics from a dumpcs method

    rawmethod: the raw content of the dumpcs method

    Return:
        list of generics in the dumpcs method
    """
    # Get the generics section of the dumpcs method
    if not dumpcsobject_method_isgenericinstmethod(rawmethod):
        # No generics
        return []
    suffix = readafter("\t/* GenericInstMethod :", rawmethod)
    genericssection = readbefore("\n\t*/", suffix)
    genericdelimiter = "\n\t|\n"
    # Split genericssection by ", ", which can be used to mark the start of each generic
    rawgenerics = genericssection.split(genericdelimiter)
    if not rawgenerics:
        # No generics
        return []
    # The split function will capture everything before the first generic -
    # which happens to be a newline - since we split by the delimiter that starts methods,
    # so delete that
    del rawgenerics[0]
    if not rawgenerics:
        # No generics
        return []
    # Build dictionary of generics from raw generics
    generics = []
    for rawgeneric in rawgenerics:
        types = dumpcsobject_method_generic_gettypes(rawgeneric)
        hasoffsetdata = dumpcsobject_method_generic_hasoffsetdata(rawgeneric)  # Offset -1 if not
        if hasoffsetdata:
            relativevirtualaddress = dumpcsobject_method_generic_getrelativevirtualaddress(rawgeneric)  # RVA
            virtualaddress = dumpcsobject_method_generic_getvirtualaddress(rawgeneric)  # VA
            offset = dumpcsobject_method_generic_getoffset(rawgeneric)  # Offset
        else:
            relativevirtualaddress = None  # RVA
            virtualaddress = None  # VA
            offset = None  # Offset
        generic = {
            "raw": rawgeneric,
            "types": types,
            "hasoffsetdata": hasoffsetdata,
            "relativevirtualaddress": relativevirtualaddress,
            "virtualaddress": virtualaddress,
            "offset": offset,
        }
        generics.append(generic)
    return generics


@cache
def dumpcsobject_method_generic_hasoffsetdata(rawgeneric: str) -> bool:
    # Not Done
    lines = getlines(rawgeneric)
    offsetdataline = readafter("\t|-", lines[0]).strip()
    if  "Offset: " not in offsetdataline:
        return False
    if "Offset: -1" in offsetdataline:
        hasoffsetdata = False
    else:
        hasoffsetdata = True
    if hasoffsetdata:
        assert "RVA: " in offsetdataline
        assert "VA: " in offsetdataline
    return hasoffsetdata


@cache
def dumpcsobject_method_generic_getrelativevirtualaddress(rawgeneric: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_generic_hasoffsetdata(rawgeneric):
        return None
    lines = getlines(rawgeneric)
    offsetdataline = readafter("\t|-", lines[0]).strip()
    suffix = readafter("RVA: ", offsetdataline)
    # if " " in suffix:
    #     relativevirtualaddress = readbefore(" ", suffix)
    # else:
    #     relativevirtualaddress = suffix
    relativevirtualaddress = readbefore(" ", suffix, mustcontain=False)
    return relativevirtualaddress


@cache
def dumpcsobject_method_generic_getoffset(rawgeneric: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_generic_hasoffsetdata(rawgeneric):
        return None
    lines = getlines(rawgeneric)
    offsetdataline = readafter("\t|-", lines[0]).strip()
    suffix = readafter("Offset: ", offsetdataline)
    # if " " in suffix:
    #     offset = readbefore(" ", suffix)
    # else:
    #     offset = suffix
    offset = readbefore(" ", suffix, mustcontain=False)
    return offset


@cache
def dumpcsobject_method_generic_getvirtualaddress(rawgeneric: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_generic_hasoffsetdata(rawgeneric):
        return None
    lines = getlines(rawgeneric)
    offsetdataline = readafter("\t|-", lines[0]).strip()
    suffix = readafter("VA: ", offsetdataline)
    # if " " in suffix:
    #     virtualaddress = readbefore(" ", suffix)
    # else:
    #     virtualaddress = suffix
    virtualaddress = readbefore(" ", suffix, mustcontain=False)
    return virtualaddress


@cache
def dumpcsobject_method_generic_gettypes(rawgeneric: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of types from a dumpcs method generic

    rawgeneric: the raw content of the dumpcs method generic

    Return:
        list of types in the dumpcs method generic
    """
    lines = getlines(rawgeneric)
    typedatalines = lines[1:-1]
    types = []
    for fulltype in typedatalines:
        hasname = dumpcsobject_method_generic_type_hasname(fulltype)
        name = dumpcsobject_method_generic_type_getname(fulltype) if hasname else None
        datatype = dumpcsobject_method_generic_type_getdatatype(fulltype)
        # Type is capitalized because "type" is a keyword
        Type = {
            "raw": fulltype,
            "hasname": hasname,
            "name": name,
            "datatype": datatype,
            }
        types.append(Type)
    return types


@cache
def dumpcsobject_method_generic_type_getdatatype(fulltype: str) -> str:
    # Not Done
    typedata = readafter("\t|-", fulltype)
    # Match generics, but not compiler generated symbols
    # EX: IEnumerator<object>, but not TweenRunner.<Start>
    suffix = readafter("(?!^)(?<!\.)<(?!>)", typedata, regex=True)
    datatype = readbefore("(?<!\<)>", suffix, regex=True, backward=True)
    return datatype


@cache
def dumpcsobject_method_generic_type_hasname(fulltype: str) -> bool:
    # Not Done
    typedata = readafter("\t|-", fulltype)
    # Match generics, but not compiler generated symbols
    # EX: # EX: IEnumerator<object>, but not TweenRunner.<Start>
    prefix = readbefore("(?!^)(?<!\.)<(?!>)", typedata, regex=True)
    suffix = readafter("(?<!\<)>", typedata, regex=True, backward=True)
    return prefix + suffix != ""


@cache
def dumpcsobject_method_generic_type_getname(fulltype: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_generic_type_hasname(fulltype):
        # No name
        return None
    typedata = readafter("\t|-", fulltype)
    # Match generics, but not compiler generated symbols
    # EX: IEnumerator<object>, but not TweenRunner.<Start>
    prefix = readbefore("(?!^)(?<!\.)<(?!>)", typedata, regex=True)
    suffix = readafter("(?<!\<)>", typedata, regex=True, backward=True)
    typename = prefix + suffix
    return typename

@cache
def dumpcsobject_method_getparams(rawmethod: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of params from a dumpcs method

    rawmethod: the raw content of the dumpcs method

    Return:
        list of params in the dumpcs object
    """
    # Get the params section of the dumpcs method
    lines = getlines(rawmethod)
    methodsignatureline = lines[1].strip()
    suffix = readafter("(", methodsignatureline)
    paramssection = readbefore(")", suffix, backward=True)
    # Split paramssection by ", ", which can be used to mark the start of each param
    # Make sure not to split by ", " in data types (such as Dict<string, int>)
    # or in strings (such as "string separator = ","")
    rawparams = []
    thisparam = ""
    previousletter = None
    instring = False
    datatypelayer = 0
    iterable = iter(paramssection)
    for letter in iterable:
        if instring:
            if (previousletter is None or previousletter != "\\") and \
            (letter == "\"" or letter == "'"):
                instring = False
        else:
            if (previousletter is None or previousletter != "\\") and \
            (letter == "\"" or letter == "'"):
                instring = True
            elif datatypelayer >= 1 and letter == ">":
                datatypelayer -= 1
            elif letter == "<":
                datatypelayer += 1
            elif datatypelayer == 0 and letter == ",":
                # Call next() on iterator to skip the character after this one (space)
                rawparams.append(thisparam)
                thisparam = ""
                next(iterable)
                # Continue to prevent this letter (",") from being added to this param
                continue
        thisparam += letter
        previousletter = letter
    if thisparam != "":
        # Add last parameter (it did not get added because there is no comma after it)
        rawparams.append(thisparam)
    if not rawparams:
        # No params
        return []
    # Build dictionary of params from raw params
    params = []
    for rawparam in rawparams:
        hasname = dumpcsobject_method_param_hasname(rawparam)
        name = dumpcsobject_method_param_getname(rawparam) if hasname else None
        datatype = dumpcsobject_method_param_getdatatype(rawparam)
        hasdefault = dumpcsobject_method_param_hasdefault(rawparam)
        default = dumpcsobject_method_param_getdefault(rawparam) if hasdefault else None
        param = {
            "raw": rawparam,
            "hasname": hasname,
            "name": name,
            "datatype": datatype,
            "hasdefault": hasdefault,
            "default": default,
        }
        params.append(param)
    return params


@cache
def dumpcsobject_method_param_hasname(rawparam: str) -> bool:
    # Not Done
    if dumpcsobject_method_param_hasdefault(rawparam):
        rawparam = readbefore(" = ", rawparam)
    if rawparam[-1] == " " or rawparam[-1] == ">":
        # EX: "(AggregateException )" or "(object <p0>)"
        hasname = False
    else:
        hasname = True
    return hasname


@cache
def dumpcsobject_method_param_getname(rawparam: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_param_hasname(rawparam):
        # No Name
        return None
    if dumpcsobject_method_param_hasdefault(rawparam):
        # the " = " always comes before the default value,
        # so we do not have to worry if the default value is a string containing " = "
        rawparam = readbefore(" = ", rawparam)
    words = getwords(rawparam, customregex="(?<!,) ")
    assert len(words) > 1
    # The name of the param is the last word
    return words[-1]


@cache
def dumpcsobject_method_param_getdatatype(rawparam: str) -> str:
    # Not Done
    if dumpcsobject_method_param_hasdefault(rawparam):
        # the " = " always comes before the default value,
        # so we do not have to worry if the default value is a string containing " = "
        rawparam = readbefore(" = ", rawparam)
    words = getwords(rawparam, customregex="(?<!,) ")
    if dumpcsobject_method_param_hasname(rawparam):
        # The data type is everything but the last word (which is the param name)
        assert len(words) > 1
        del words[-1]
    # Concatenate the words back into a string
    datatype = wordstostring(words)
    return datatype


@cache
def dumpcsobject_method_param_hasdefault(rawparam: str) -> bool:
    # Not Done
    # the " = " always comes before the default value,
    # so we do not have to worry if the default value is a string containing " = "
    return " = " in rawparam


@cache
def dumpcsobject_method_param_getdefault(rawparam: str) -> str:
    # Not Done
    if not dumpcsobject_method_param_hasdefault(rawparam):
        # No default
        return None
    # the " = " always comes before the default value,
    # so we do not have to worry if the default value is a string containing " = "
    default = readafter(" = ", rawparam)
    return default


@cache
def dumpcsobject_hasconstructor(rawobject: str) -> bool:
    # Not Done
    methods = dumpcsobject_getmethods(rawobject)
    for method in methods:
        if method["isconstructor"]:
            return True
    return False


@cache
def dumpcsobject_hasstaticconstructor(rawobject: str) -> bool:
    # Not Done
    methods = dumpcsobject_getmethods(rawobject)
    for method in methods:
        if method["isstaticconstructor"]:
            return True
    return False


@cache
def dumpcsobject_getupdatetypes(rawobject: str) -> list[str]:
    # Not Done
    updatetypes = []
    methods = dumpcsobject_getmethods(rawobject)
    for method in methods:
        if method["isupdate"]:
            if not method["updatetype"] in updatetypes:
                updatetypes.append(method["updatetype"])
    return updatetypes


@cache
def dumpcsobject_getfields(rawobject: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of fields from a dumpcs object

    rawobject: the raw content of the dumpcs object

    Return:
        list of fields in the dumpcs object
    """
    # Get the fields section of the dumpcs object
    if not dumpcsobject__hasfields(rawobject):
        # No Fields
        return []
    suffix = readafter("\n\t// Fields", rawobject)
    checks = ("\n\t// Properties", "\n\t// Methods")
    found = False
    for check in checks:
        if check in suffix:
            fieldssection = readbefore(f"\n{check}", suffix)
            found = True
            break
    if not found:
        fieldssection = readbefore("\n}", suffix, backward=True)
    fielddelimiter = "\n"
    # Split fields by "\n", which can be used to mark the start of each field
    rawfields = fieldssection.split(fielddelimiter)
    if not rawfields:
        return []
    # The split function will capture everything before the first field
    # since we split by the delimiter that starts fields, so delete that
    del rawfields[0]
    # Build dictionary of fields from raw fields
    fields = []
    for rawfield in rawfields:
        name = dumpcsobject_field_getname(rawfield)
        datatype = dumpcsobject_field_getdatatype(rawfield)
        #isstatic = dumpcsobject_field_isstatic(rawfield)
        isdynamic = dumpcsobject_field_isdynamic(rawfield)
        isgeneric = dumpcsobject_field_isgeneric(rawfield)
        generictypename = dumpcsobject_field_getgenerictypename(rawfield) if isgeneric else None
        hasoffset = dumpcsobject_field_hasoffset(rawfield)
        offset = dumpcsobject_field_getoffset(rawfield) if hasoffset else None
        hasdefault = dumpcsobject_field_hasdefault(rawfield)
        default = dumpcsobject_field_getdefault(rawfield) if hasdefault else None
        field = {
            "raw": rawfield,
            "name": name,
            "datatype": datatype,
            "isdynamic": isdynamic,
            "hasoffset": hasoffset,
            "offset": offset,
            "isgeneric": isgeneric,
            "generictypename": generictypename,
            "hasdefault": hasdefault,
            "default": default,
                }
        fields.append(field)
    return fields


@cache
def dumpcsobject_field_getname(rawfield: str) -> str:
    # Not Done
    fieldsignatureline = rawfield.strip()
    prefix = readbefore(";", fieldsignatureline)
    if dumpcsobject_field_hasdefault(rawfield):
        prefix = readbefore(" = ", prefix)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # The name of the field is the last word before the delimiter in the rawfield
    lastword = words[-1]
    if dumpcsobject_field_isgeneric(rawfield):
        # Match generics, but not compiler generated symbols
        # EX: IEnumerator<object>, but not TweenRunner.<Start>
        prefix = readbefore("(?!^)(?<!\.)<(?!>)", lastword, regex=True)
        suffix = readafter("(?<!\<)>", lastword, regex=True, backward=True)
        name = prefix + suffix
    else:
        name = lastword
    return name


@cache
def dumpcsobject_field_isgeneric(rawfield: str) -> bool:
    # Not Done
    fieldsignatureline = rawfield.strip()
    prefix = readbefore(";", fieldsignatureline)
    if dumpcsobject_field_hasdefault(rawfield):
        prefix = readbefore(" = ", prefix)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    lastword = words[-1]
    # Match generics, but not compiler generated symbols
    # EX: IEnumerator<object>, but not TweenRunner.<Start>
    if re.search("(?!^)(?<!\.)<(?!>)", lastword):
        return True
    else:
        return False


@cache
def dumpcsobject_field_getgenerictypename(rawfield: str) -> str:
    # Not Done
    if not dumpcsobject_field_isgeneric(rawfield):
        # No generic type
        return None
    fieldsignatureline = rawfield.strip()
    prefix = readbefore(";", fieldsignatureline)
    if dumpcsobject_field_hasdefault(rawfield):
        prefix = readbefore(" = ", prefix)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # The name of the field is the last word before the delimiter in the rawfield
    name = words[-1]
    suffix = readafter("<", name)
    generictype = readbefore(">", suffix, backward=True)
    return generictype


@cache
def dumpcsobject_field_getvisibility(rawfield: str) -> str:
    # Not Done
    fieldsignatureline = rawfield.strip()
    prefix = readbefore(";", fieldsignatureline)
    if dumpcsobject_field_hasdefault(rawfield):
        prefix = readbefore(" = ", prefix)
    # The data type is everything but the last word (which is the field name)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # Delete field name
    del words[-1]
    # Concatenate the words back into a string
    datatype = wordstostring(words)
    return datatype


@cache
def dumpcsobject_field_getdatatype(rawfield: str) -> str:
    # Not Done
    fieldsignatureline = rawfield.strip()
    prefix = readbefore(";", fieldsignatureline)
    if dumpcsobject_field_hasdefault(rawfield):
        prefix = readbefore(" = ", prefix)
    # The data type is everything but the last word (which is the field name)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # Delete field name
    del words[-1]
    # Concatenate the words back into a string
    datatype = wordstostring(words)
    return datatype


@cache
def dumpcsobject_field_isdynamic(rawfield: str) -> bool:
    # Not Done
    datatype = dumpcsobject_field_getdatatype(rawfield)
    # Split the data type by " "
    # Make sure not to split by " " in compound types (such as Dict<string, int>)
    words = getwords(datatype, customregex="(?<!,) ") # This regex will match " " unless it is prefixed by ","
    assert len(words) > 1
    return "dynamic" in words


@cache
def dumpcsobject_field_hasoffset(rawfield: str) -> bool:
    # Not Done
    fieldsignatureline = rawfield.strip()
    suffix = readafter(";", fieldsignatureline, backward=True)
    return "// " in suffix


@cache
def dumpcsobject_field_getoffset(rawfield: str) -> str:
    # Not Done
    if not dumpcsobject_field_hasoffset(rawfield):
        # No offset
        return None
    fieldsignatureline = rawfield.strip()
    suffix = readafter(";", fieldsignatureline, backward=True)
    offset = readafter("// ", suffix)
    return offset


@cache
def dumpcsobject_field_hasdefault(rawfield: str) -> bool:
    # Not Done
    # the " = " always comes before the default value,
    # so we do not have to worry if the default value is a string containing " = "
    return " = " in rawfield


@cache
def dumpcsobject_field_getdefault(rawfield: str) -> str:
    # Not Done
    if not dumpcsobject_field_hasdefault(rawfield):
        # No default
        return None
    fieldsignatureline = rawfield.strip()
    prefix = readbefore(";", fieldsignatureline, backward=True)
    # the " = " always comes before the default value,
    # so we do not have to worry if the default value is a string containing " = "
    default = readafter(" = ", prefix)
    return default


@cache
def dumpcsobject_getproperties(rawobject: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of properties from a dumpcs object

    rawobject: the raw content of the dumpcs object

    Return:
        list of properties in the dumpcs object
    """
    # Get the properties section of the dumpcs object
    if not dumpcsobject__hasproperties(rawobject):
        # No Properties
        return []
    suffix = readafter("\n\t// Properties", rawobject)
    checks = ("\n\t// Methods", "\n\t// Fields")
    found = False
    for check in checks:
        if check in suffix:
            propertiessection = readbefore(f"\n{check}", suffix)
            found = True
            break
    if not found:
        propertiessection = readbefore("\n}", suffix, backward=True)
    propertydelimiter = "\n"
    # Split properties by "\n", which can be used to mark the start of each property
    rawproperties = propertiessection.split(propertydelimiter)
    if not rawproperties:
        return []
    # The split function will capture everything before the first property
    # since we split by the delimiter that starts properties, so delete that
    del rawproperties[0]
    # Build dictionary of properties from raw properties
    properties = []
    for rawproperty in rawproperties:
        name = dumpcsobject_property_getname(rawproperty)
        datatype = dumpcsobject_property_getdatatype(rawproperty)
        # Fixme: Can you override properties?
        isoverride = dumpcsobject_property_isoverride(rawproperty)
        isvirtual = dumpcsobject_property_isvirtual(rawproperty)
        isabstract = True if dumpcsobject_isabstract(rawobject) else dumpcsobject_property_isabstract(rawproperty)
        #isstatic = dumpcsobject_property_isstatic(rawproperty)
        isgeneric = dumpcsobject_property_isgeneric(rawproperty)
        generictypename = dumpcsobject_property_getgenerictypename(rawproperty) if isgeneric else None
        hasgetter = dumpcsobject_property_hasgetter(rawproperty)
        hassetter = dumpcsobject_property_hassetter(rawproperty)
        # The name Property is capitalized because property" is a keyword in python
        Property = {
            "raw": rawproperty,
            "name": name,
            "datatype": datatype,
            "isvirtual": isvirtual,
            "isabstract": isabstract,
            "isoverride": isoverride,
            "isgeneric": isgeneric,
            "generictypename": generictypename,
            "hasgetter": hasgetter,
            "hassetter": hassetter,
        }
        properties.append(Property)
    return properties


@cache
def dumpcsobject_property_getname(rawproperty: str) -> str:
    # Not Done
    propertysignatureline = rawproperty.strip()
    prefix = readbefore(" {", propertysignatureline)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # The name of the property is the last word before the delimiter in the rawproperty
    lastword = words[-1]
    if dumpcsobject_property_isgeneric(rawproperty):
        # Match generics, but not compiler generated symbols
        # EX: IEnumerator<object>, but not TweenRunner.<Start>
        prefix = readbefore("(?!^)(?<!\.)<(?!>)", lastword, regex=True)
        suffix = readafter("(?<!\<)>", lastword, regex=True, backward=True)
        name = prefix + suffix
    else:
        name = lastword
    return name


@cache
def dumpcsobject_property_isgeneric(rawproperty: str) -> str:
    # Not Done
    propertysignatureline = rawproperty.strip()
    prefix = readbefore(" {", propertysignatureline)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    lastword = words[-1]
    # Match generics, but not compiler generated symbols
    # EX: IEnumerator<object>, but not TweenRunner.<Start>
    if re.search("(?!^)(?<!\.)<(?!>)", lastword):
        return True
    else:
        return False

@cache
def dumpcsobject_property_getgenerictypename(rawproperty: str) -> str:
    # Not Done
    if not dumpcsobject_property_isgeneric(rawproperty):
        # No generic type
        return None
    propertysignatureline = rawproperty.strip()
    prefix = readbefore(" {", propertysignatureline)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    # The name of the property is the last word before the delimiter in the rawproperty
    lastword = words[-1]
    suffix = readafter("<", lastword)
    generictype = readbefore(">", suffix, backward=True)
    return generictype


@cache
def dumpcsobject_property_getdatatype(rawproperty: str) -> str:
    # Not Done
    propertysignatureline = rawproperty.strip()
    prefix = readbefore(" {", propertysignatureline)
    # The data type is everything but the last word (which is the property name)
    words = getwords(prefix, customregex="(?<!,) ")
    assert len(words) > 1
    del words[-1]
    # Concatenate the words back into a string
    datatype = wordstostring(words)
    return datatype


@cache
def dumpcsobject_property_isvirtual(rawproperty: str) -> bool:
    # Not Done
    datatype = dumpcsobject_property_getdatatype(rawproperty)
    return datatype_isvirtual(datatype)

@cache
def dumpcsobject_property_isabstract(rawproperty: str) -> bool:
    # Not Done
    datatype = dumpcsobject_property_getdatatype(rawproperty)
    return datatype_isabstract(datatype)


@cache
def dumpcsobject_property_isoverride(rawproperty: str) -> bool:
    # Not Done
    datatype = dumpcsobject_property_getdatatype(rawproperty)
    return datatype_isoverride(datatype)


@cache
def dumpcsobject_property_getpropertymethods(rawproperty: str) -> str:
    propertysignatureline = rawproperty.strip()
    suffix = readafter(" { ", propertysignatureline)
    propertymethodssection = readbefore(" }", suffix, backward=True)
    propertymethods = [propertymethod.strip() for propertymethod in propertymethodssection.split(";")]
    # The split function will capture everything after the last property
    # since we split by the delimiter that ends properties,
    # so delete that
    del propertymethods[-1]
    return propertymethods


@cache
def dumpcsobject_property_hasgetter(rawproperty: str) -> bool:
    # Not Done
    propertymethods = dumpcsobject_property_getpropertymethods(rawproperty)
    return "get" in propertymethods

@cache
def dumpcsobject_property_hassetter(rawproperty: str) -> bool:
    # Not Done
    propertymethods = dumpcsobject_property_getpropertymethods(rawproperty)
    return "set" in propertymethods


def dumpcs_getobjects(dumpcs: str,
                      objecttypefilter: Optional[set[str]]=None,
                      namespacefilter: Optional[set[str]]=None,
                      customfilter: Optional[Callable]=None,
                      makeobjectpaths=False,
                      getmethodhex=True,
                      libfilepath=None) -> list[dict]:
    # Not Done
    """
    Docs Not Done!
    Possible Improvements:
        1. Creating a new list is inefficient, modifying existing list would be ideal
        2. Directly using dumpcs.split() instead of using rawobjects variable may be faster,
        but sacrifices readability and simplicity
        3. Having different loops for namespacefilter, objecttypefilter, customfilter, and combinations
        is faster, but logner
        4. Directly creating a dictionary may be faster than using variables for namespacefilter
        and objecttypefilter, but sacrifices readability and simplicity
        5. To save memory and speed, maybe only add object base if it exists rather than adding None.
        However, this sacrifices readability and simplicity
        6. To save memory and speed, maybe only add object type model if it exists rather than adding None.
        However, this sacrifices readability and simplicity
        7. Returning a dictionary of objects by path (namespace -> object) may be faster and simpler than
        returning a list of dictionaries (as to grab an object out of the list by its path, the list must be
        iterated through until a match is found), but a list is simpler, easier, and faster to create,
        process, and iterate over
        8. Object delimiter should be a constant
        9. Supplying raw content and objectcache parameters to all functions, whether they use them or not,
        is good for consistency, readability, and refactoring, but sacrifices speed and memory

    Parses dumpcs file into a list of objects
    Does not remove blank lines

    Arguments:
        dumpcs: the raw content of the dumpcs file
        createtypemodels: whether to create type models for objects
        objecttypefilter: filter to only process objects of certain types (set to None to disable filter)
        namespacefilter: filter to only process objects that are in certain namespaces (inclusive)
        (set to None to disable filter, set to [None] to only process objects in global namespace)
        customfilter: filter that is supplied the finished object dictionary and tells the function to only
        process objects that satisfy custom conditions (set to None to disable filter)
        getmethodhex: whether to get the hex code of methods from the binary
        libfilepath: the file path of the libil2cpp.so binary

    Return:
        list of parsed objects from the dumpcs file
        :param makeobjectpaths:
    """
    if getmethodhex:
        raise NotImplementedError("getmethodhex is not done!")
    if getmethodhex and libfilepath is None:
        raise IllegalArgumentException("Call to dumpcs_getobjects with" \
                                        "getmethodhex enabled but no libfilepath.")
    objectdelimiter = "// Namespace: "
    if dumpcs_hasattributes(dumpcs):
        dumpcs = dumpcs_removeattributes(dumpcs)
    # Split dumpcs by "// Namespace: ", which can be used to mark the start of each object
    # There are blank lines between objects, so add on a blank line
    rawobjects = dumpcs.split(f"\n{objectdelimiter}")
    #if not rawobjects:
    #    # If there aren't any objects in dumpcs (this is impossible, but just theoretically),
    #    # we can terminate the function now
    #    return []
    if not rawobjects:
        # exceptions.errors.unexpecteddumpcsformat(f"Error go brrrr")
        raise UnexpectedDumpcsFormatError("No objects in dumpcs", dumpcs)
    # The split function will capture everything before the first object
    # since we split by the delimiter that starts objects, so delete that
    del rawobjects[0]
    # Build dictionary of objects from raw objects
    objects = []
    for count, rawobject in enumerate(rawobjects):
        # Add "// Namespace: " back on, as string.split excludes the delimiter
        rawobject = objectdelimiter + rawobject

        hasnamespace = dumpcsobject_hasnamespace(rawobject)
        namespace = dumpcsobject_getnamespace(rawobject) if hasnamespace else None
        if namespacefilter and namespace not in namespacefilter:
            continue

        objecttype = dumpcsobject_getobjecttype(rawobject)
        if objecttypefilter and objecttype not in objecttypefilter:
            continue

        isabstract = dumpcsobject_isabstract(rawobject)
        isstatic = dumpcsobject_isstatic(rawobject)
        issealed = dumpcsobject_issealed(rawobject)
        isinherited = dumpcsobject_isinherited(rawobject)
        name = dumpcsobject_getname(rawobject, includenesting=False)
        isnested = dumpcsobject_isnested(rawobject)
        nesting = dumpcsobject_getnesting(rawobject, includename=False, innertoouter=True)
        datatype = dumpcsobject_getdatatype(rawobject)
        bases = dumpcsobject_getbases(rawobject) if isinherited else None
        isgeneric = dumpcsobject_isgeneric(rawobject)
        generictypename = dumpcsobject_getgenerictypename(rawobject) if isgeneric else None
        typedefindex = dumpcsobject_gettypedefindex(rawobject)

        hasmethods = dumpcsobject__hasmethods(rawobject)
        methods = dumpcsobject_getmethods(rawobject) if hasmethods else []
        hasconstructor = dumpcsobject_hasconstructor(rawobject) if hasmethods else False
        hasstaticconstructor = dumpcsobject_hasstaticconstructor(rawobject) if hasmethods else False
        updatetypes = dumpcsobject_getupdatetypes(rawobject) if hasmethods else []

        hasfields = dumpcsobject__hasfields(rawobject)
        fields = dumpcsobject_getfields(rawobject) if hasfields else []
        hasproperties = dumpcsobject__hasproperties(rawobject)
        properties = dumpcsobject_getproperties(rawobject) if hasproperties else []

        # The name Object is capitalized because "object" is a keyword
        Object = {
            "raw": rawobject,
            "name": name,
            "typedefindex": typedefindex,
            "objecttype": objecttype,
            "hasnamespace": hasnamespace,
            "namespace": namespace,
            "datatype": datatype,
            "isinherited": isinherited,
            "bases": bases,
            "isnested": isnested,
            "nesting": nesting,
            "isgeneric": isgeneric,
            "generictypename": generictypename,
            "hasmethods": hasmethods,
            "methods": methods,
            "hasconstructor": hasconstructor,
            "hasstaticconstructor": hasstaticconstructor,
            "updatetypes": updatetypes,
            "hasfields": hasfields,
            "fields": fields,
            "hasproperties": hasproperties,
            "properties": properties,
        }
        if makeobjectpaths:
            path = dumpcsobject_getpath(rawobject)
            Object["path"] = path
        # Now that we have all the object's data, we can check against custom filter.
        if customfilter and not(customfilter(Object)):
            continue
        objects.append(Object)
        percentdone = (count * 10000 // len(rawobjects)) / 100
        if percentdone != 0 and percentdone % 1 == 0:
            print(f"{percentdone}%")
    return objects


def dumpcs_getimages(dumpcs: str) -> list[dict]:
    # Not Done
    """
    Docs Not Done!
    Possible Improvements:
    """
    raise NotImplementedError("dumpcs_getimages function is unfinished")


dumpcspath, encoding = r"C:\Users\zachy\OneDrive\Documents\Work\Projects\Polywar\64bit\dump.cs", 'utf8'
#dumpcspath, encoding = r"C:\Users\zachy\OneDrive\Documents\Work\Projects\Pixel Gun
# 3D\Pixel Gun 3D
# 16.6.1\Pixel Gun
# 3D 16.6.1 dump.cs", 'utf8'
outputpath = r"C:\Users\zachy\PycharmProjects\UnityDeobfuscator\tests\parseddumpcs.json"
#outputpath = r"C:\Users\zachy\OneDrive\Documents\Work\Temp\Python Temps\parseddumpcs.json"
if __name__ == "__main__":
    with open(dumpcspath,encoding = encoding) as f:
        #import cProfile
        #cProfile.run("dumpcs_getobjects(dumpcs_removeattributes(f.read()), makeobjectpaths=True, getmethodhex=False)")
        #sys.exit()
        objects = dumpcs_getobjects(dumpcs_removeattributes(f.read()), makeobjectpaths=True,
                                             getmethodhex=False)
    with open(outputpath,'w',encoding = encoding) as f:
        # We can't write all the objects to the file because it's too big and eats up all my memory
        # when I try to view it
        # For testing purposes, only a few hundred is necessary
        #f.write(str(objects))
        #for i in objects:
            #if i["name"] == "FriendsMenu":
            #if "ResourceFallbackManage" in i["name"]:
                #f.write(str(i))
                #sys.exit()
        f.write(str(objects[1000:1300]))
