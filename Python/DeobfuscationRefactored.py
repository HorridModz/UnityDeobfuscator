from __future__ import annotations
import sys
import os
import warnings
import copy
from typing import *
import string
import re
import json
from functools import cache, lru_cache
from typing import Any
from unitydeobfuscatorexceptions import *
import fileutils


filehandler = fileutils.FileHandler()
def removeattributes(*args, **kwargs):
    """
    Function has been removed
    """
    raise NotImplementedError("removeattributes function has been removed.\
     Attributes are removed from the whole dumpcs, so the call to removeattributes can be deleted.")


def removewhitespace(*args, **kwargs):
    """
    Function has been removed
    """
    raise NotImplementedError("removewhitespace function has been removed.\
         To trim whitespace, use the trim function. To remove all whitespace, use the removeallwhitespace funnction.")


def getobjects(*args, **kwargs):
    """
    Function has been removed
    """
    raise NotImplementedError("getobjects function has been removed.\
         To get objects, use dumpcs_getobjects directly on dumpcs.")


def getfullobjects(*args, **kwargs):
    """
    Function has been removed
    """
    raise NotImplementedError("getfullobjects function has been removed.\
             To get objects, use dumpcs_getobjects directly on dumpcs.")


def readaftersubstring(sub: str, s: str, backwards=False, mustcontain=True, lengthwarning=True) -> str:
    # Done
    """
    Todo: Regex Support, Update Docs
    This function is based off of
    https://stackoverflow.com/questions/12572362/how-to-get-a-string-after-a-specific-substring/57064170#57064170

    Possible Improvements:
        1.  Directly returning instead of using suffix variable may be faster, but sacrifices
        readability and simplicity

    Returns the substring after the delimiter
    If the substring is not found in the string, returns the whole string

    Example:
        String: "Split this string by delimiter"
        Sub:    "string"
        Return: " by delimiter"

    Arguments:
        s: string to split
        sub: delimiter to read after
        lengthwarning: whether to throw a warning if the arguments do not make sense (this is purely
        to catch bugs)

    Return:
        the partition of the string that comes after the delimiter
    """
    if lengthwarning and len(sub) > len(s):
        warnings.warn(f"Call to readaftersubstring(sub={sub}, str={s}): substring is longer than full string",
                      SyntaxWarning)
    if mustcontain:
        assert sub in s
    if backwards:
        prefix, found, suffix = s.rpartition(sub)
    else:
        prefix, found, suffix = s.partition(sub)
    if not found:
        suffix = prefix
    return suffix


def readbeforesubstring(sub: str, s: str, backwards=False, mustcontain=True, lengthwarning=True) -> str:
    # Done
    """
    Todo: Regex Support, Update Docs
    This function is based off of
    https://stackoverflow.com/questions/12572362/how-to-get-a-string-after-a-specific-substring/57064170#57064170

    Possible Improvements:
        1.  Directly returning instead of using prefix variable may be faster, but sacrifices
        readability and simplicity

    Returns the substring before the delimiter
    If the substring is not found in the string, returns the whole string

    Example:
        String: "Split this string by delimiter"
        Sub:    "string"
        Return: "Split this "

    Arguments:
        s: string to split
        sub: delimiter to read before
        lengthwarning: whether to throw a warning if the arguments do not make sense (this is purely
        to catch bugs)

    Return:
        the partition of the string that comes before the delimiter
    """
    if lengthwarning and len(sub) > len(s):
        warnings.warn(f"Call to readbeforesubstring(sub={sub}, str={s}): substring is longer than full string",
                      SyntaxWarning)
    if mustcontain:
        assert sub in s
    if backwards:
        prefix, found, suffix = s.rpartition(sub)
    else:
        prefix, found, suffix = s.partition(sub)
    if not found:
        prefix = suffix
    return prefix


def removesubstring(sub: str, s: str) -> str:
    # Done
    """
    Possible Improvements:

    Removes all occurrences of one substring from a string

    Example:
        String: "Removing Substrings"
        Sub:    "ing"
        Return: "Remov Substrs"

    Arguments:
        s: string to remove substring from
        sub: substring to remove from string

    Return:
        string with substring removed
    """
    return s.replace(sub, "")


def removesubstrings(s: str, subs: list[str]) -> str:
    # Done
    """
    Possible Improvements:

    Removes all occurrences of multiple substrings from a string, in order of the list of substrings

    Example:
        String: "Removing Substrings"
        Subs:    ["e","in","ing"]
        Return: "Rmovg Substrgs"

    Arguments:
        s: string to remove substrings from
        subs: list of substrings to remove from string

    Return:
        string with substrings removed
    """
    for sub in subs:
        s = removesubstring(s, sub)
    return s


def replacesubstring(s: str, sub: str, replace: str) -> str:
    # Done
    """
    Possible Improvements:

    Replaces all occurrences of one substring in a string

    Example:
        String:  "Replacing Substrings"
        Sub:     "ing"
        Replace: "ed"
        Return: "Replaced Substreds"

    Arguments:
        s: string to replace substring in
        sub: substring to replace
        replace: what to replace substring with

    Return:
        string with substring replaced with replace
    """
    return s.replace(sub, replace)


def replacesubstrings(s: str, subs: list[str], replace: str) -> str:
    # Done
    """
    Possible Improvements:

    Replaces all occurrences of multiple substrings in a string, in order of the list of substrings

    Example:
        String:  "Replacing Substrings"
        Subs:     ["e","in","ing"]
        Replace: "c"
        Return: "Rcplaccg Substrcgs"

     Arguments:
        s: string to replace substrings in
        subs: list of substrings to remove in string
        replace: what to replace substring with

    Return:
        string with substrings replaced with replace
    """
    for sub in subs:
        s = replacesubstring(s, sub, replace)
    return s


def removeallwhitespace(s: str) -> str:
    # Done
    # NOTE: Function is named removeallwhitespace because old function removewhitespace
    # was for trimming. Once all functions use trim instead, this function can be renamed
    # back to removewhitespace.
    """
    Possible Improvements:
        Make whitespace a constant instead of unpacking each time function is called

    Removes all whitespace from a string
    Does not just trim leading and trailing. For that, use the trim function.

    Example:
        String: "   Whitespace  will be      removed from
        this string"
        Return: "Whitespacewillberemovedfromthisstring"

    Arguments:
        s: string to remove whitespace from

    Return:
        string with whitespace removed
    """
    # Should have a constant instead of unpacking
    # string.whitespace each time
    _whitespace = [*string.whitespace]
    return removesubstrings(s, _whitespace)


def removeblanklines(s: str) -> str:
    # Done
    """
    Possible Improvements:

    Removes all blank lines from a string
    This function does not remove lines with only whitespace!

    Example:
        String: "
        blank
            lines will be

            removed from

            thisstr
         ing"
        Return: "blank
            lines will be
            removed from
            thisstr
         ing"

    Arguments:
        s: string to remove blank lines from

    Return:
        string with blank lines removed
    """
    return replacesubstring(s, "\n\n", "\n")


def iswhitespace(s: str, totreatblankaswhitespace=True) -> bool:
    # Done
    """
    Possible Improvements:

    Detects if a string is all whitespace
    Works on strings with any length, including 0

    Example:
        String: "
             "
        Return: True

        String: "   hello world!
            hi"
        Return: false

    Arguments:
        s: string to check for whitespace
        totreatblankaswhitespace: whether to treat "" as whitespace

    Return:
        whether string is all whitespace
    """
    if s == "":
        return totreatblankaswhitespace
    else:
        return s.isspace()


def trim(s: str, leading=True, trailing=True) -> str:
    """
    Possible Improvements:

    Trims whitespace from a string

    Example:
        String: "   hello world!
        "
        Leading: True
        Trailing: True
        Return: "hello world!"

    Arguments:
        s: string to trim whitespace from
        leading: whether to trim leading whitespace
        trailing: whether to trim trailing whitespace

    Return:
        string with trimmed whitespace
    """
    if leading and trailing:
        return s.strip()
    elif leading:
        return s.lstrip()
    elif trailing:
        return s.rstrip()
    else:
        return s


def getwords(s: str) -> list[str]:
    # Done
    """
    Possible Improvements:
        1. Creating a new list is inefficient, modifying existing list would be ideal
        2. Directly using s.split() instead of using words variable may be faster, but
        sacrifices readability  and simplicity  and simplicity


    Splits a string into a list of words
    Treats any type of whitespace as a word delimiter, including new lines and tabs
    Treats chunks of whitespace as delimiters (ex: 2 spaces has the same effect as 1 space)

    Example:
        String: "the quick
                    brown       fox

                 abcdefg  "
        Return: ["the","quick","brown","fox","abcdefg"]

    Arguments:
        s: string to split into words

    Return:
        list of the string's words
    """
    return s.split()


def wordstostring(words: list[str],
                  totrimwords=False,
                  toignoreblankwords=True,
                  toignorewhitespacewords=False,
                  concatenator=" ") -> str:
    # Done
    """
    Possible Improvements:
        1. Creating a new list is inefficient, modifying existing list would be ideal

    joins a list of words into a string

    Example:
        words: ["hello","a","b","   ","cd\n","","hey",""]
        concatenator: " "
        toignoreblankwords: false
        totrimwords: false
        toignorewhitespacewords: false
        Return: "hello a b     cd
                   hey "

    Arguments:
        words: list of words to join into a string
        toignoreblankwords: whether to concatenate or ignore blank words
        totrimwords: whether to trim leading and trailing whitespace from each word
        (only leading / only trailing whitespace is not supported)
        toignorewhitespacewords: whether to concatenate or ignore words with only whitespace
        concatenator: the string to put in between words (default space)

    Return:
        all the words concatenated by concatenator (default space)
    """
    if not(toignoreblankwords or toignorewhitespacewords or totrimwords):
        return concatenator.join(words)
    else:
        wordstoconcatenate = []
        for word in words:
            if iswhitespace(word) and toignorewhitespacewords:
                continue
            if totrimwords:
                word = trim(word, True, True)
            if not (word == "" and toignoreblankwords):
                wordstoconcatenate.append(word)
        return concatenator.join(wordstoconcatenate)


def getlines(s: str,
             toremoveblanklines=False,
             totrimlines=False) -> list[str]:
    # Done
    """
    Possible Improvements:
        1. Creating a new list is inefficient, modifying existing list would be ideal
        2. Directly using s.splitlines() instead of using lines variable may be faster,
        but sacrifices readability  and simplicity  and simplicity

    Splits a string into a list of lines

    Example:
        String: "a

                    b

                 c  "
        toremoveblanklines: True
        totrimlines: True
        Return: ["a","b","c"]

    Arguments:
        s: string to split into lines
        toremoveblanklines: whether to ignore lines that are blank or only whitespace
        totrimlines: whether to trim leading and trailing whitespace from each line
        (only leading / only trailing whitespace is not supported)

    Return:
        list of the string's lines
    """
    lines = s.splitlines()
    if toremoveblanklines or totrimlines:
        newlines = []
        for line in lines:
            if totrimlines:
                line = trim(line, True, True)
            if not (toremoveblanklines and iswhitespace(line)):
                newlines.append(line)
        return newlines
    else:
        return lines


def linestostring(lines: list[str],
                  totrimlines=False,
                  toignoreblanklines=False) -> str:
    # Done
    """
    Possible Improvements:

    joins a list of lines into a string

    Example:
        lines: ["a","","b","    ","cd",""]
        toignoreblanklines: False
        totrimlines: False
        Return: "a

                 b

                 cd
                 "

    Arguments:
        lines: list of lines to join into a string
        toignoreblanklines: whether to concatenate or ignore lines that are blank or only whitespace
        totrimlines: whether to trim leading and trailing whitespace from each line
        (only leading / only trailing whitespace is not supported)

    Return:
        all the lines concatenated by new line
    """
    return wordstostring(lines, totrimlines, toignoreblanklines, toignoreblanklines, "\n")


def datatype_getbase(datatype: str) -> str:
    # Not Done
    # One-word type: Bool, int, float, user-defined type, etc...
    if " " in datatype:
        # Split the data type by " "
        # Make sure not to split by " " in compound types (such as Dict<string, int>)
        words = re.split("(?<!,) ", datatype) # This regex will match " " unless it is prefixed by ","
        # The base data type is the last word of the data type
        basedatatype = words[-1]
    else:
        basedatatype = datatype
    return basedatatype


def dumpcs_isvalid(dumpcs: str) -> bool:
    #Not done
    """
    Bad detection, needs proper algorithm

    Determines whether a dumpcs file is valid
    Works by checking against some substrings that some should exist in all valid dump.cs files
    All dumpcs files entered should be valid, but of course they must be checked.
    Note: This function only performs a short check on the file as a whole.
    On the other hand, the dumpcs_checkformat function analyzes the whole thing and is very picky.

    Arguments:
        dumpcs: the content of the dumpcs file

    Return:
        whether the dumpcs is valid
    """
    checks = ("// Image 0:", "// Namespace: ", "class", "\n\t// Methods", "// RVA: 0x")
    for check in checks:
        if check not in dumpcs:
            return False
    return True


def dumpcs_checkformat(dumpcs: str) -> list[dict]:
    #Not done
    """
    Scan dump.cs for unexpected formatting
    Returns list of unexpected formatting errors

    Arguments:
        dumpcs: the content of the dumpcs file

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
        dumpcs: the content of the dumpcs file
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
            if not (trimmedline == "" or trimmedline[0] != "["):
                return True
        return False


def dumpcs_constructor(path: str) -> str:
    # Done
    """
    Possible Improvements:
        1. Setting dumpcs variable after removing attributes makes code more readable and concise,
        but is less inefficient than directing passing result of dumpcs_removeattributes.
        In addition, attributes must be removed before dumpcs is checked for format errors
        2. Directly using dumpcs_removeattributes instead of checking with dumpcs_hasattributes may be faster
        (idk if it is), but it sacrifices readability

    Loads and initializes a dumpcs file

    Arguments:
        path: the file path of the dumpcs file

    Return:
        the contents of the dump.cs file
    """
    dumpcs = filehandler.read_file(path)
    if not dumpcs_isvalid(dumpcs):
        raise InvalidDumpcsError(path)
    if dumpcs_hasattributes(dumpcs):
        dumpcs = dumpcs_removeattributes(dumpcs)
    formaterrors = dumpcs_checkformat(dumpcs)
    if formaterrors:
        #exceptions.warnings.unexpecteddumpcsformatearly(path,formaterrors)
        for formaterror in formaterrors:
            raise UnexpectedDumpcsFormatError(formaterror.message, formaterror.sample, line=formaterror.line)
    return dumpcs


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
        dumpcs: the content of the dumpcs file

    Return:
        dumpcs content with attributes removed
   """
    lines = getlines(dumpcs, False, False)
    newlines = []
    for line in lines:
        #Trim leading whitespace from line
        trimmedline = trim(line, True, False)
        # If the first non-whitespace character on the line is a square bracket,
        # this means the line is an attribute
        if trimmedline == "" or trimmedline[0] != "[":
            #The line is not an attribute line, so keep it
            newlines.append(line)
    return linestostring(newlines, False, False)


def dumpcsobject_hasnamespace(fullobject: str) -> bool:
    # Not Done
    lines = getlines(fullobject)
    namespaceline = lines[0]
    return namespaceline != "// Namespace: "


def dumpcsobject_getnamespace(fullobject: str) -> Optional[str]:
    # Done
    """

    Possible Improvements:

    Gets the namespace of a dumpcs object

    Example:
        namespaceline: // Namespace: Microsoft.Win32
        Return: Microsoft.Win32


    Arguments:
        fullobject: the content of the dumpcs object

    Return:
        namespace of the dumpcs sobject
    """
    if not dumpcsobject_hasnamespace(fullobject):
        # No namespace
        return None
    lines = getlines(fullobject)
    namespaceline = lines[0]
    # Everything after "// Namespace: " in the namespaceline is the object's namespace
    namespacedelimiter = "// Namespace: "
    namespace = readaftersubstring(namespacedelimiter, namespaceline)
    return namespace


def dumpcsobject_gettype(fullobject: str) -> str:
    # Done
    """

    Possible Improvements:
        1.  Directly returning instead of using type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        2. Object types should be a constant
        3. IDK if using a dictionary cache is faster or ironically slower

    Gets the type (struct, class, enum, or interface) of a dumpcs object

    Example:
        objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: class


    Arguments:
        fullobject: the content of the dumpcs object

    Return:
        type of the dumpcs object
    """
    lines = getlines(fullobject)
    objectdeclarationline = lines[1]
    objectdeclarationline = objectdeclarationline.strip()
    # Find the first word that is a valid type of object in the object declaration line
    # This is the type of the object
    OBJECTTYPES = {"class", "struct", "interface", "enum"}  # should be a constant!
    words = getwords(objectdeclarationline)
    assert len(words) > 1
    for word in words:
        if word in OBJECTTYPES:
            return word
    # Object type (class, struct, enum, interface) not found
    #exceptions.errors.unexpecteddumpcsformat(f"Could not find type of object:\n{objectdeclarationline}")
    raise UnexpectedDumpcsFormatError("Could not find type of object", fullobject)


def dumpcsobject_getdatatype(fullobject: str) -> str:
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
        objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: public static


    Arguments:
        fullobject: the content of the dumpcs object

    Return:
        data type of the dumpcs object
    """
    # Find everything before the first word that is a valid type of object in the object declaration line
    # This is the data type of the object
    lines = getlines(fullobject)
    objectdeclarationline = lines[1]
    objectdeclarationline = objectdeclarationline.strip()
    # Find the first word that is a valid type of object in the object declaration line
    # This is the type of the object
    OBJECTTYPES = {"class", "struct", "interface", "enum"}  # should be a constant!
    words = getwords(objectdeclarationline)
    assert len(words) > 1
    datatypewords = []
    for word in words:
        if word in OBJECTTYPES:
            # Concatenate the words back into a string
            datatype = wordstostring(datatypewords)
            return datatype
        else:
            # Add this word onto the data type
            datatypewords.append(word)
    # Object type (class, struct, enum, interface) not found
    #exceptions.errors.unexpecteddumpcsformat(f"Could not find type of object:\n{objectdeclarationline}")
    raise UnexpectedDumpcsFormatError("Could not find type of object", fullobject)


def dumpcsobject_getname(fullobject: str, includenesting=False) -> str:
    # Done
    """

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets the name of a dumpcs object

    Examples:
        objectdeclarationline: private enum SimpleCollator.ExtenderType // TypeDefIndex: 41
        includenesting: True
        Return: SimpleCollator.ExtenderType

        objectdeclarationline: private enum SimpleCollator.ExtenderType // TypeDefIndex: 41
        includenesting: False
        Return: ExtenderType


    Arguments:
        fullobject: the content of the dumpcs object
        includenesting: whether to include the outer objects in the name
        (only applies if the object is nested)

    Return:
        the name of the dumpcs object
    """
    lines = getlines(fullobject)
    objectdeclarationline = lines[1]
    objectdeclarationline = objectdeclarationline.strip()
    if dumpcsobject_isinherited(fullobject):
        # If the object is inherited, read before the base class (to get the derived class)
        prefix = readbeforesubstring(" : ", objectdeclarationline)
    else:
        # If the object is not inherited, read before the typedefindex
        prefix = readbeforesubstring(" //", objectdeclarationline)
    if dumpcsobject_isgeneric(fullobject):
        #EX: We want Lookup.Grouping, not Lookup.Grouping<TKey, TElement>
        TEMPREPLACEMENT = "***TEMPREPLACEMENT***"  # Should be a constant!
        TEMPREPLACEMENT2 = "***TEMPREPLACEMENTNUMBER2***"  # Should be a constant!
        assert TEMPREPLACEMENT not in prefix
        tempreplaced = prefix.replace("<>", TEMPREPLACEMENT)
        assert TEMPREPLACEMENT2 not in tempreplaced
        tempreplaced = tempreplaced.replace(".<", TEMPREPLACEMENT2)
        prefix = readbeforesubstring("<", tempreplaced)
        prefix = prefix.replace(TEMPREPLACEMENT, "<>")
        prefix = prefix.replace(TEMPREPLACEMENT2, ".<")
    # The name of the object is the last word before the delimiter in the objectdeclarationline
    words = getwords(prefix)
    assert len(words) > 1
    fullname = words[-1] #including nesting (if any)
    if includenesting:
        name = fullname
    else:
        nesting = fullname.split(".")
        # Last element is the name of the object (without nesting, if any)
        name = nesting[-1]
    return name


def dumpcsobject_getbase(fullobject: str) -> Optional[str]:
    # Done
    """
    Docs Not Done!

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets the base class of a dumpcs object
    If the object is not inherited, returns None

    Examples:
        objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: None

        objectdeclarationline: public class DecalsMeshRenderer : MonoBehaviour // TypeDefIndex: 4727
        Return: MonoBehavior


    Arguments:
        fullobject: the content of the dumpcs object

    Returns:
        base class of the dumpcs object, or None if the dumpcs object is not inherited
    """
    lines = getlines(fullobject)
    objectdeclarationline = lines[1]
    objectdeclarationline = objectdeclarationline.strip()
    if not dumpcsobject_isinherited(fullobject):
        return None
    suffix = readaftersubstring(" : ", objectdeclarationline)
    prefix = readbeforesubstring(" //", suffix)
    if dumpcsobject_isgenericbase(fullobject):
        #EX: We want Lookup.Grouping, not Lookup.Grouping<TKey, TElement>
        TEMPREPLACEMENT = "***TEMPREPLACEMENT***"  # Should be a constant!
        assert TEMPREPLACEMENT not in suffix
        tempreplaced = suffix.replace("<>", TEMPREPLACEMENT)
        prefix = readbeforesubstring("<", tempreplaced)
        prefix = prefix.replace(TEMPREPLACEMENT, "<>")
    base = prefix
    return base


def dumpcsobject_getnesting(fullobject: str, includename=False, innertoouter=True) -> tuple:
    # Not Done
    # Ex: a.b.c -> (c, b, a)
    fullname = dumpcsobject_getname(fullobject, includenesting=True) # including nesting (if any)
    nesting = fullname.split(".")
    if not includename:
        # Remove last element as this is the name of the object (without nesting, if any)
        del nesting[-1]
    if innertoouter:
        # Reverse the list to make the order go from inner to outer rather than outer to inner
        nesting.reverse()
    return tuple(nesting)


def dumpcsobject_isnested(fullobject: str) -> bool:
    nesting = dumpcsobject_getnesting(fullobject)
    if nesting:
        return True
    else:
        return False


def dumpcsobject_getpath(fullobject: str) -> str:
    hasnamespace = dumpcsobject_hasnamespace(fullobject)
    namespace = dumpcsobject_getnamespace(fullobject)
    name = dumpcsobject_getname(fullobject)
    nesting = dumpcsobject_getnesting(fullobject, includename=False, innertoouter=False)
    path = ""
    if hasnamespace:
        path += f"{namespace}::"
    for nestinglevel in nesting:
        path += f"{nestinglevel}."
    path += name
    return path


@lru_cache(maxsize=1, typed=True)
def dumpcsobject_isgeneric(fullobject: str) -> bool:
    # Not Done
    lines = getlines(fullobject)
    objectdeclarationline = lines[1]
    objectdeclarationline = objectdeclarationline.strip()
    if dumpcsobject_isinherited(fullobject):
        # If the object is inherited, read before the base class (to get the derived class)
        prefix = readbeforesubstring(" : ", objectdeclarationline)
    else:
        # If the object is not inherited, read before the typedefindex
        prefix = readbeforesubstring(" //", objectdeclarationline)
    TEMPREPLACEMENT = "***TEMPREPLACEMENT***"  # Should be a constant!
    TEMPREPLACEMENT2 = "***TEMPREPLACEMENTNUMBER2***"  # Should be a constant!
    assert TEMPREPLACEMENT not in prefix
    tempreplaced = prefix.replace("<>", TEMPREPLACEMENT)
    assert TEMPREPLACEMENT2 not in tempreplaced
    tempreplaced = tempreplaced.replace(".<", TEMPREPLACEMENT2)
    words = getwords(tempreplaced)
    assert len(words) > 1
    # We don't want classes like <Module>
    if "<" in tempreplaced and not words[-1].startswith("<"):
        isgeneric = True
    else:
        isgeneric = False
    return isgeneric


def dumpcsobject_getgenericdatatype(fullobject: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_isgeneric(fullobject):
        # Not generic
        return None
    lines = getlines(fullobject)
    objectdeclarationline = lines[1]
    objectdeclarationline = objectdeclarationline.strip()
    if dumpcsobject_isinherited(fullobject):
        # If the object is inherited, read before the base class (to get the derived class)
        prefix = readbeforesubstring(" : ", objectdeclarationline)
    else:
        # If the object is not inherited, read before the typedefindex
        prefix = readbeforesubstring(" //", objectdeclarationline)
    TEMPREPLACEMENT = "***TEMPREPLACEMENT***"  # Should be a constant!
    assert TEMPREPLACEMENT not in prefix
    tempreplaced = prefix.replace("<>", TEMPREPLACEMENT)
    suffix = readaftersubstring("<", tempreplaced)
    prefix = readbeforesubstring(">", suffix, backwards=True)
    genericdatatype = prefix.replace(TEMPREPLACEMENT,"<>")
    return genericdatatype


@lru_cache(maxsize=1, typed=True)
def dumpcsobject_isgenericbase(fullobject: str) -> bool:
    # Not Done
    lines = getlines(fullobject)
    objectdeclarationline = lines[1]
    objectdeclarationline = objectdeclarationline.strip()
    assert dumpcsobject_isinherited(fullobject)
    suffix = readaftersubstring(" : ", objectdeclarationline)
    prefix = readbeforesubstring(" //", suffix)
    TEMPREPLACEMENT = "***TEMPREPLACEMENT***"  # Should be a constant!
    TEMPREPLACEMENT2 = "***TEMPREPLACEMENTNUMBER2***"  # Should be a constant!
    assert TEMPREPLACEMENT not in prefix
    tempreplaced = prefix.replace("<>", TEMPREPLACEMENT)
    assert TEMPREPLACEMENT2 not in tempreplaced
    tempreplaced = tempreplaced.replace(".<", TEMPREPLACEMENT2)
    # We don't want classes like <Module>
    if "<" in tempreplaced and not tempreplaced.startswith("<"):
        isgenericbase = True
    else:
        isgenericbase = False
    return isgenericbase


def dumpcsobject_gettypedefindex(fullobject: str) -> str:
    # Done
    """

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets the typedefindex of a dumpcs object

    Example:
        objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: 4

    Arguments:
        fullobject: the content of the dumpcs object

    Return:
        typedefindex of the dumpcs object
    """
    lines = getlines(fullobject)
    objectdeclarationline = lines[1]
    objectdeclarationline = objectdeclarationline.strip()
    typedefindex = readaftersubstring("// TypeDefIndex: ", objectdeclarationline)
    return typedefindex


def dumpcsobject_isinherited(fullobject: str) -> bool:
    # Done
    """

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Determines whether a dumpcs object is inherited

    Examples:
        objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: False

        objectdeclarationline: public class DecalsMeshRenderer : MonoBehaviour // TypeDefIndex: 4727
        Return: True

    Arguments:
        fullobject: the content of the dumpcs object

    Return:
        whether the dumpcs object is inherited
    """
    lines = getlines(fullobject)
    objectdeclarationline = lines[1]
    objectdeclarationline = objectdeclarationline.strip()
    return " : " in objectdeclarationline


def dumpcsobject_hasmethods(fullobject: str) -> bool:
    return "\n\t// Methods" in fullobject


def dumpcsobject_hasfields(fullobject: str) -> bool:
    return "\n\t// Fields" in fullobject


def dumpcsobject_hasproperties(fullobject: str) -> bool:
    return "\n\t// Properties" in fullobject


@lru_cache(maxsize=1, typed=True)
def dumpcsobject_getmethods(fullobject: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of methods from a dumpcs object
    Includes list of generics in each method

    fullobject: the content of the dumpcs object

    Return:
        list of methods in the dumpcs object
    """
    # Get the methods section of the dumpcs object
    if not dumpcsobject_hasmethods(fullobject):
        # No Methods
        return []
    suffix = readaftersubstring("\n\t// Methods", fullobject)
    checks = ("\n\t// Fields", "\n\t// Properties")
    found = False
    for check in checks:
        if check in suffix:
            methodssection = readbeforesubstring(f"\n{check}", suffix)
            found = True
            break
    if not found:
        methodssection = readbeforesubstring("\n}", suffix, backwards=True)
    methoddelimiter = "\n\n"
    # Split methodssection by "\n\n", which can be used to mark the start of each method
    fullmethods = methodssection.split(methoddelimiter)
    if not fullmethods:
        return []
    # The split function will capture everything before the first method
    # since we split by the delimiter that starts methods, so delete that
    del fullmethods[0]
    # Build dictionary of methods from full methods
    methods = []
    for fullmethod in fullmethods:
        isconstructor = dumpcsobject_method_isconstructor(fullmethod)
        isstaticconstructor = dumpcsobject_method_isstaticconstructor(fullmethod)
        isoperator = dumpcsobject_method_isoperator(fullmethod)
        isupdate = dumpcsobject_method_isupdate(fullmethod)
        if isupdate:
            updatetype = dumpcsobject_method_getupdatetype(fullmethod)
        else:
            updatetype = None
        if isconstructor or isstaticconstructor:
            name = dumpcsobject_getname(fullobject, includenesting=False)
        else:
            name = dumpcsobject_method_getname(fullmethod)
        datatype = dumpcsobject_method_getdatatype(fullmethod)
        basedatatype = datatype_getbase(datatype)
        isvoid = dumpcsobject_method_isvoid(fullmethod)
        isoverride = dumpcsobject_method_isoverride(fullmethod)
        isvirtual = dumpcsobject_method_isvirtual(fullmethod)
        hasslot = dumpcsobject_method_hasslot(fullmethod)
        if hasslot:
            slot = dumpcsobject_method_getslot(fullmethod)
        else:
            slot = None
        isgeneric = dumpcsobject_method_isgeneric(fullmethod)
        if isgeneric:
            generics = dumpcsobject_method_getgenerics(fullmethod)
        else:
            #generics = None
            generics = []
        hasgenericdatatype = dumpcsobject_method_hasgenericdatatype(fullmethod)
        if hasgenericdatatype:
            genericdatatype = dumpcsobject_method_getgenericdatatype(fullmethod)
        else:
            genericdatatype = None
        hasoffsetdata = dumpcsobject_method_hasoffsetdata(fullmethod) # Offset -1 if not
        if hasoffsetdata:
            relativevirtualaddress = dumpcsobject_method_getrelativevirtualaddress(fullmethod) #RVA
            virtualaddress = dumpcsobject_method_getvirtualaddress(fullmethod) #VA
            offset = dumpcsobject_method_getoffset(fullmethod) #Offset
        else:
            relativevirtualaddress = None  # RVA
            virtualaddress = None  # VA
            offset = None  # Offset
        params = dumpcsobject_method_getparams(fullmethod)
        method = {
            "content": fullmethod,
            "name": name,
            "isconstructor": isconstructor,
            "isstaticconstructor": isstaticconstructor,
            "isoperator": isoperator,
            "isupdate": isupdate,
            "updatetype": updatetype,
            "datatype": datatype,
            "basedatatype": basedatatype,
            "isvoid": isvoid,
            "isvirtual": isvirtual,
            "isoverride": isoverride,
            "hasslot": hasslot,
            "slot": slot,
            "hasoffsetdata": hasoffsetdata,
            "relativevirtualaddress": relativevirtualaddress,
            "offset": offset,
            "virtualaddress": virtualaddress,
            "params": params,
            "isgeneric": isgeneric,
            "generics": generics,
            "hasgenericdatatype": hasgenericdatatype,
            "genericdatatype": genericdatatype,
                }
        methods.append(method)
    return methods


def dumpcsobject_method_getname(fullmethod: str) -> str:
    # Not Done
    lines = getlines(fullmethod)
    methoddeclarationline = lines[1]
    methoddeclarationline = methoddeclarationline.strip()
    prefix = readbeforesubstring("(", methoddeclarationline)
    words = getwords(prefix)
    assert len(words) > 1
    # The name of the method is the last word before the delimiter in the methoddeclarationline
    lastword = words[-1]
    if dumpcsobject_method_hasgenericdatatype(fullmethod):
        assert "<" in lastword
        prefix = readbeforesubstring("<", lastword)
        assert ">" in lastword
        suffix = readaftersubstring(">", lastword, backwards=True)
        name = prefix + suffix
    else:
        name = lastword
    return name


def dumpcsobject_method_isconstructor(fullmethod: str) -> bool:
    # Not Done
    name = dumpcsobject_method_getname(fullmethod)
    return name == ".ctor"


def dumpcsobject_method_isstaticconstructor(fullmethod: str) -> bool:
    # Not Done
    name = dumpcsobject_method_getname(fullmethod)
    return name == ".cctor"


def dumpcsobject_method_isoperator(fullmethod: str) -> bool:
    # Not Done
    name = dumpcsobject_method_getname(fullmethod)
    #OPERATORNAMES = {"+", "-", "*", "/", "%"} # Should be a constant!
    # return name in OPERATORNAMES
    raise NotImplementedError("operatornames list is unfinished")


def dumpcsobject_method_isupdate(fullmethod: str) -> bool:
    # Not Done
    name = dumpcsobject_method_getname(fullmethod)
    UPDATENAMES = {"FixedUpdate", "LateUpdate", "Update"} # Should be a constant!
    return name in UPDATENAMES


def dumpcsobject_method_getupdatetype(fullmethod: str) -> str:
    # Not Done
    if dumpcsobject_method_isupdate(fullmethod):
        name = dumpcsobject_method_getname(fullmethod)
        UPDATENAMES = {"FixedUpdate", "LateUpdate", "Update"}  # Should be a constant!
        assert name in UPDATENAMES
        return name
    else:
        # No update type
        return None


def dumpcsobject_method_hasgenericdatatype(fullmethod: str) -> str:
    # Not Done
    lines = getlines(fullmethod)
    methoddeclarationline = lines[1]
    methoddeclarationline = methoddeclarationline.strip()
    prefix = readbeforesubstring("(", methoddeclarationline)
    words = getwords(prefix)
    assert len(words) > 1
    # The name of the method is the last word before the delimiter in the methoddeclarationline
    name = words[-1]
    return "<" in name

def dumpcsobject_method_getgenericdatatype(fullmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_hasgenericdatatype(fullmethod):
        # No generic type
        return None
    lines = getlines(fullmethod)
    methoddeclarationline = lines[1]
    methoddeclarationline = methoddeclarationline.strip()
    prefix = readbeforesubstring("(", methoddeclarationline)
    words = getwords(prefix)
    assert len(words) > 1
    # The name of the method is the last word before the delimiter in the methoddeclarationline
    name = words[-1]
    suffix = readaftersubstring("<", name)
    generictype = readbeforesubstring(">", suffix, backwards=True)
    return generictype


@lru_cache(maxsize=1, typed=True)
def dumpcsobject_method_getdatatype(fullmethod: str) -> str:
    # Not Done
    lines = getlines(fullmethod)
    methoddeclarationline = lines[1]
    methoddeclarationline = methoddeclarationline.strip()
    prefix = readbeforesubstring("(", methoddeclarationline)
    # The data type is everything but the last word (which is the method name)
    words = getwords(prefix)
    assert len(words) > 1
    del words[-1]
    # Concatenate the words back into a string
    datatype = wordstostring(words)
    return datatype


def dumpcsobject_method_isvoid(fullmethod: str) -> bool:
    # Not Done
    datatype = dumpcsobject_method_getdatatype(fullmethod)
    basedatatype = datatype_getbase(datatype)
    return basedatatype == "void"


def dumpcsobject_method_isvirtual(fullmethod: str) -> bool:
    # Not Done
    datatype = dumpcsobject_method_getdatatype(fullmethod)
    words = getwords(datatype)
    assert words
    return "virtual" in words


def dumpcsobject_method_isoverride(fullmethod: str) -> bool:
    # Not Done
    datatype = dumpcsobject_method_getdatatype(fullmethod)
    words = getwords(datatype)
    assert words
    return "override" in words


def dumpcsobject_method_hasslot(fullmethod: str) -> bool:
    # Not Done
    lines = getlines(fullmethod)
    offsetdataline = lines[0]
    offsetdataline = offsetdataline.strip()
    return "Slot: " in offsetdataline


def dumpcsobject_method_getslot(fullmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_hasslot(fullmethod):
        # No slot
        return None
    lines = getlines(fullmethod)
    offsetdataline = lines[0]
    offsetdataline = offsetdataline.strip()
    suffix = readaftersubstring("Slot: ", offsetdataline)
    if " " in suffix:
        slot = readbeforesubstring(" ", suffix)
    else:
        slot = suffix
    return slot

def dumpcsobject_method_isgeneric(fullmethod: str) -> bool:
    # Not Done
    return "\t/* GenericInstMethod :" in fullmethod


def dumpcsobject_method_hasoffsetdata(fullmethod: str) -> bool:
    # Not Done
    lines = getlines(fullmethod)
    offsetdataline = lines[0]
    offsetdataline = offsetdataline.strip()
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


def dumpcsobject_method_getrelativevirtualaddress(fullmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_hasoffsetdata(fullmethod):
        return None
    lines = getlines(fullmethod)
    offsetdataline = lines[0]
    offsetdataline = offsetdataline.strip()
    suffix = readaftersubstring("RVA: ", offsetdataline)
    if " " in suffix:
        relativevirtualaddress = readbeforesubstring(" ", suffix)
    else:
        relativevirtualaddress = suffix
    return relativevirtualaddress


def dumpcsobject_method_getoffset(fullmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_hasoffsetdata(fullmethod):
        return None
    lines = getlines(fullmethod)
    offsetdataline = lines[0]
    offsetdataline = offsetdataline.strip()
    suffix = readaftersubstring("Offset: ", offsetdataline)
    if " " in suffix:
        offset = readbeforesubstring(" ", suffix)
    else:
        offset = suffix
    return offset


def dumpcsobject_method_getvirtualaddress(fullmethod: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_hasoffsetdata(fullmethod):
        return None
    lines = getlines(fullmethod)
    offsetdataline = lines[0]
    offsetdataline = offsetdataline.strip()
    suffix = readaftersubstring("VA: ", offsetdataline)
    if " " in suffix:
        virtualaddress = readbeforesubstring(" ", suffix)
    else:
        virtualaddress = suffix
    return virtualaddress


def dumpcsobject_method_getgenerics(fullmethod: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of generics from a dumpcs method

    fullmethod: the content of the dumpcs method

    Return:
        list of generics in the dumpcs method
    """
    # Get the generics section of the dumpcs method
    if not dumpcsobject_method_isgeneric(fullmethod):
        # No generics
        return []
    suffix = readaftersubstring("\t/* GenericInstMethod :", fullmethod)
    genericssection = readbeforesubstring("\n\t*/", suffix)
    genericdelimiter = "\n\t|\n"
    # Split genericssection by ", ", which can be used to mark the start of each generic
    fullgenerics = genericssection.split(genericdelimiter)
    if not fullgenerics:
        # No generics
        return []
    # The split function will capture everything before the first generic -
    # which happens to be a newline - since we split by the delimiter that starts methods,
    # so delete that
    del fullgenerics[0]
    if not fullgenerics:
        # No generics
        return []
    # Build dictionary of generics from full generics
    generics = []
    for fullgeneric in fullgenerics:
        types = dumpcsobject_method_generic_gettypes(fullgeneric)
        hasoffsetdata = dumpcsobject_method_generic_hasoffsetdata(fullgeneric)  # Offset -1 if not
        if hasoffsetdata:
            relativevirtualaddress = dumpcsobject_method_generic_getrelativevirtualaddress(fullgeneric)  # RVA
            virtualaddress = dumpcsobject_method_generic_getvirtualaddress(fullgeneric)  # VA
            offset = dumpcsobject_method_generic_getoffset(fullgeneric)  # Offset
        else:
            relativevirtualaddress = None  # RVA
            virtualaddress = None  # VA
            offset = None  # Offset
        generic = {
            "content": fullgeneric,
            "types": types,
            "hasoffsetdata": hasoffsetdata,
            "relativevirtualaddress": relativevirtualaddress,
            "virtualaddress": virtualaddress,
            "offset": offset,
        }
        generics.append(generic)
    return generics


def dumpcsobject_method_generic_hasoffsetdata(fullgeneric: str) -> bool:
    # Not Done
    lines = getlines(fullgeneric)
    offsetdataline = lines[0]
    offsetdataline = readaftersubstring("\t|-", offsetdataline).strip()
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


def dumpcsobject_method_generic_getrelativevirtualaddress(fullgeneric: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_generic_hasoffsetdata(fullgeneric):
        return None
    lines = getlines(fullgeneric)
    offsetdataline = lines[0]
    offsetdataline = readaftersubstring("\t|-", offsetdataline).strip()
    suffix = readaftersubstring("RVA: ", offsetdataline)
    if " " in suffix:
        relativevirtualaddress = readbeforesubstring(" ", suffix)
    else:
        relativevirtualaddress = suffix
    return relativevirtualaddress


def dumpcsobject_method_generic_getoffset(fullgeneric: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_generic_hasoffsetdata(fullgeneric):
        return None
    lines = getlines(fullgeneric)
    offsetdataline = lines[0]
    offsetdataline = readaftersubstring("\t|-", offsetdataline).strip()
    suffix = readaftersubstring("Offset: ", offsetdataline)
    if " " in suffix:
        offset = readbeforesubstring(" ", suffix)
    else:
        offset = suffix
    return offset


def dumpcsobject_method_generic_getvirtualaddress(fullgeneric: str) -> Optional[str]:
    # Not Done
    if not dumpcsobject_method_generic_hasoffsetdata(fullgeneric):
        return None
    lines = getlines(fullgeneric)
    offsetdataline = lines[0]
    offsetdataline = readaftersubstring("\t|-", offsetdataline).strip()
    suffix = readaftersubstring("VA: ", offsetdataline)
    if " " in suffix:
        virtualaddress = readbeforesubstring(" ", suffix)
    else:
        virtualaddress = suffix
    return virtualaddress

def dumpcsobject_method_generic_gettypes(fullgeneric: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of types from a dumpcs method generic

    fullgeneric: the content of the dumpcs method generic

    Return:
        list of types in the dumpcs method generic
    """
    lines = getlines(fullgeneric)
    typedatalines = lines[1:-1]
    types = []
    for fulltype in typedatalines:
        hasname = dumpcsobject_method_generic_type_hasname(fulltype)
        if hasname:
            name = dumpcsobject_method_generic_type_getname(fulltype)
        else:
            name = None
        datatype = dumpcsobject_method_generic_type_getdatatype(fulltype)
        # Type is capitalized because "type" is a keyword
        Type = {
            "content": fulltype,
            "hasname": hasname,
            "name": name,
            "datatype": datatype,
                            }
        types.append(Type)
    return types


def dumpcsobject_method_generic_type_getdatatype(fulltype: str) -> str:
    # Not Done
    typedata = readaftersubstring("\t|-", fulltype)
    # EX: LinqHelpers.<>c__DisplayClass0_0<object>..ctor
    # We want to get <object>, not <>
    TEMPREPLACEMENT = "***TEMPREPLACEMENT***"  # Should be a constant!
    assert TEMPREPLACEMENT not in typedata
    tempreplaced = typedata.replace("<>", TEMPREPLACEMENT)
    suffix = readaftersubstring("<", tempreplaced)
    prefix = readbeforesubstring(">", suffix, backwards=True)
    datatype = prefix.replace(TEMPREPLACEMENT, "<>")
    return datatype


def dumpcsobject_method_generic_type_hasname(fulltype: str) -> bool:
    # Not Done
    typedata = readaftersubstring("\t|-", fulltype)
    TEMPREPLACEMENT = "***TEMPREPLACEMENT***"  # Should be a constant!
    assert TEMPREPLACEMENT not in typedata
    tempreplaced = typedata.replace("<>", TEMPREPLACEMENT)
    return ">." in tempreplaced


def dumpcsobject_method_generic_type_getname(fulltype: str) -> str:
    # Not Done
    if not dumpcsobject_method_generic_type_hasname(fulltype):
        # No name
        return None
    typedata = readaftersubstring("\t|-", fulltype)
    TEMPREPLACEMENT = "***TEMPREPLACEMENT***"  # Should be a constant!
    assert TEMPREPLACEMENT not in typedata
    tempreplaced = typedata.replace("<>", TEMPREPLACEMENT)
    prefix = readbeforesubstring("<", tempreplaced)
    suffix = readaftersubstring(">", tempreplaced, backwards=True)
    typename = (prefix + suffix).replace(TEMPREPLACEMENT, "<>")
    return typename


def dumpcsobject_method_getparams(fullmethod: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of params from a dumpcs method

    fullmethod: the content of the dumpcs method

    Return:
        list of params in the dumpcs object
    """
    # Get the params section of the dumpcs method
    lines = getlines(fullmethod)
    methoddeclarationline = lines[1]
    methoddeclarationline = methoddeclarationline.strip()
    suffix = readaftersubstring("(", methoddeclarationline)
    paramssection = readbeforesubstring(")", suffix, backwards=True)
    # Split paramssection by ", ", which can be used to mark the start of each param
    # Make sure not to split by ", " in data types (such as Dict<string, int>)
    # or in strings (such as string seperator ",")
    fullparams = []
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
                fullparams.append(thisparam)
                thisparam = ""
                next(iterable)
                # Continue to prevent this letter (",") from being added to this param
                continue
        thisparam += letter
        previousletter = letter
    if thisparam != "":
        # Add last parameter (it did not get added because there is no comma after it)
        fullparams.append(thisparam)
    if not fullparams:
        # No params
        return []
    # Build dictionary of params from full params
    params = []
    for fullparam in fullparams:
        hasname = dumpcsobject_method_param_hasname(fullparam)
        if hasname:
            name = dumpcsobject_method_param_getname(fullparam)
        else:
            name = None
        datatype = dumpcsobject_method_param_getdatatype(fullparam)
        basedatatype = datatype_getbase(datatype)
        hasgenericdatatype = dumpcsobject_method_param_hasgenericdatatype(fullparam)
        if hasgenericdatatype:
            genericdatatype = dumpcsobject_method_param_getgenericdatatype(fullparam)
        else:
            genericdatatype = None
        hasdefault = dumpcsobject_method_param_hasdefault(fullparam)
        if hasdefault:
            default = dumpcsobject_method_param_getdefault(fullparam)
        else:
            default = None
        param = {
            "content": fullparam,
            "hasname": hasname,
            "name": name,
            "datatype": datatype,
            "basedatatype": basedatatype,
            "hasgenericdatatype": hasgenericdatatype,
            "genericdatatype": genericdatatype,
            "hasdefault": hasdefault,
            "default": default,
        }
        params.append(param)
    return params


def dumpcsobject_method_param_hasname(fullparam: str) -> bool:
    # Not Done
    if dumpcsobject_method_param_hasdefault(fullparam):
        fullparam = readbeforesubstring(" = ", fullparam)
    # (type ) or generic (type <generic>)
    if fullparam[-1] == " " or fullparam[-1] == ">":
        hasname = False
    else:
        hasname = True
    return hasname


def dumpcsobject_method_param_getname(fullparam: str) -> str:
    # Not Done
    if not dumpcsobject_method_param_hasname(fullparam):
        # No Name
        return None
    if dumpcsobject_method_param_hasdefault(fullparam):
        # the " = " always comes before the default value,
        # so we do not have to worry if the default value is a string containing " = "
        fullparam = readbeforesubstring(" = ", fullparam)
    words = getwords(fullparam)
    assert len(words) > 1
    # The name of the param is the last word of the param
    lastword = words[-1]
    if dumpcsobject_method_param_hasgenericdatatype(fullparam):
        assert "<" in lastword
        prefix = readbeforesubstring("<", lastword)
        assert ">" in lastword
        suffix = readaftersubstring(">", lastword, backwards=True)
        name = prefix + suffix
    else:
        name = lastword
    return name

def dumpcsobject_method_param_hasgenericdatatype(fullparam: str) -> bool:
    # Not Done
    if dumpcsobject_method_param_hasdefault(fullparam):
        # the " = " always comes before the default value,
        # so we do not have to worry if the default value is a string containing " = "
        fullparam = readbeforesubstring(" = ", fullparam)
    words = getwords(fullparam)
    assert words
    return "<" in words[-1]


def dumpcsobject_method_param_getgenericdatatype(fullparam: str) -> str:
    # Not Done
    if not dumpcsobject_method_param_hasgenericdatatype(fullparam):
        # No generic type
        return None
    if dumpcsobject_method_param_hasdefault(fullparam):
        # the " = " always comes before the default value,
        # so we do not have to worry if the default value is a string containing " = "
        fullparam = readbeforesubstring(" = ", fullparam)
    words = getwords(fullparam)
    lastword = words[-1]
    suffix = readaftersubstring("<", lastword)
    generictype = readbeforesubstring(">", suffix, backwards=True)
    return generictype


def dumpcsobject_method_param_getdatatype(fullparam: str) -> str:
    # Not Done
    if dumpcsobject_method_param_hasdefault(fullparam):
        # the " = " always comes before the default value,
        # so we do not have to worry if the default value is a string containing " = "
        fullparam = readbeforesubstring(" = ", fullparam)
    words = getwords(fullparam)
    if dumpcsobject_method_param_hasname(fullparam):
        # The data type is everything but the last word (which is the param name)
        assert len(words) > 1
        del words[-1]
    # Concatenate the words back into a string
    datatype = wordstostring(words)
    return datatype


@lru_cache(maxsize=1, typed=True)
def dumpcsobject_method_param_hasdefault(fullparam: str) -> bool:
    # Not Done
    # the " = " always comes before the default value,
    # so we do not have to worry if the default value is a string containing " = "
    return " = " in fullparam


def dumpcsobject_method_param_getdefault(fullparam: str) -> str:
    # Not Done
    if not dumpcsobject_method_param_hasdefault(fullparam):
        # No default
        return None
    # the " = " always comes before the default value,
    # so we do not have to worry if the default value is a string containing " = "
    default = readaftersubstring(" = ", fullparam)
    return default


def dumpcsobject_hasconstructor(fullobject: str) -> bool:
    # Not Done
    methods = dumpcsobject_getmethods(fullobject)
    for method in methods:
        if method["isconstructor"]:
            return True
    return False


def dumpcsobject_hasstaticconstructor(fullobject: str) -> bool:
    # Not Done
    methods = dumpcsobject_getmethods(fullobject)
    for method in methods:
        if method["isstaticconstructor"]:
            return True
    return False


def dumpcsobject_getupdatetypes(fullobject: str) -> list[str]:
    # Not Done
    updatetypes = []
    methods = dumpcsobject_getmethods(fullobject)
    for method in methods:
        if method["isupdate"]:
            if not method["updatetype"] in updatetypes:
                updatetypes.append(method["updatetype"])
    return updatetypes


def dumpcsobject_getfields(fullobject: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of fields from a dumpcs object

    fullobject: the content of the dumpcs object

    Return:
        list of fields in the dumpcs object
    """
    # Get the fields section of the dumpcs object
    if not dumpcsobject_hasfields(fullobject):
        # No Fields
        return []
    suffix = readaftersubstring("\n\t// Fields", fullobject)
    checks = ("\n\t// Properties", "\n\t// Methods")
    found = False
    for check in checks:
        if check in suffix:
            fieldssection = readbeforesubstring(f"\n{check}", suffix)
            found = True
            break
    if not found:
        fieldssection = readbeforesubstring("\n}", suffix, backwards=True)
    fielddelimiter = "\n"
    # Split fields by "\n", which can be used to mark the start of each field
    fullfields = fieldssection.split(fielddelimiter)
    if not fullfields:
        return []
    # The split function will capture everything before the first field
    # since we split by the delimiter that starts fields, so delete that
    del fullfields[0]
    # Build dictionary of fields from full fields
    fields = []
    for fullfield in fullfields:
        name = dumpcsobject_field_getname(fullfield)
        datatype = dumpcsobject_field_getdatatype(fullfield)
        basedatatype = datatype_getbase(datatype)
        isdynamic = dumpcsobject_field_isdynamic(fullfield)
        hasgenericdatatype = dumpcsobject_field_hasgenericdatatype(fullfield)
        if hasgenericdatatype:
            genericdatatype = dumpcsobject_field_getgenericdatatype(fullfield)
        else:
            genericdatatype = None
        hasoffset = dumpcsobject_field_hasoffset(fullfield)
        if hasoffset:
            offset = dumpcsobject_field_getoffset(fullfield) #Offset
        else:
            offset = None
        hasdefault = dumpcsobject_field_hasdefault(fullfield)
        if hasdefault:
            default = dumpcsobject_field_getdefault(fullfield)
        else:
            default = None
        field = {
            "content": fullfield,
            "name": name,
            "datatype": datatype,
            "basedatatype": basedatatype,
            "isdynamic": isdynamic,
            "hasoffset": hasoffset,
            "offset": offset,
            "hasgenericdatatype": hasgenericdatatype,
            "genericdatatype": genericdatatype,
            "hasdefault": hasdefault,
            "default": default,
                }
        fields.append(field)
    return fields


def dumpcsobject_field_getname(fullfield: str) -> str:
    # Not Done
    fielddeclarationline = fullfield.strip()
    prefix = readbeforesubstring(";", fielddeclarationline)
    if dumpcsobject_field_hasdefault(fullfield):
        prefix = readbeforesubstring(" = ", prefix)
    words = getwords(prefix)
    assert len(words) > 1
    # The name of the field is the last word before the delimiter in the fullfield
    lastword = words[-1]
    if dumpcsobject_field_hasgenericdatatype(fullfield):
        assert "<" in lastword
        prefix = readbeforesubstring("<", lastword)
        assert ">" in lastword
        suffix = readaftersubstring(">", lastword, backwards=True)
        name = prefix + suffix
    else:
        name = lastword
    return name


def dumpcsobject_field_hasgenericdatatype(fullfield: str) -> bool:
    # Not Done
    fielddeclarationline = fullfield.strip()
    prefix = readbeforesubstring(";", fielddeclarationline)
    if dumpcsobject_field_hasdefault(fullfield):
        prefix = readbeforesubstring(" = ", prefix)
    words = getwords(prefix)
    assert len(words) > 1
    # The name of the field is the last word before the delimiter in the fullfield
    name = words[-1]
    return "<" in name


def dumpcsobject_field_getgenericdatatype(fullfield: str) -> str:
    # Not Done
    if not dumpcsobject_field_hasgenericdatatype(fullfield):
        # No generic type
        return None
    fielddeclarationline = fullfield.strip()
    prefix = readbeforesubstring(";", fielddeclarationline)
    if dumpcsobject_field_hasdefault(fullfield):
        prefix = readbeforesubstring(" = ", prefix)
    words = getwords(prefix)
    assert len(words) > 1
    # The name of the field is the last word before the delimiter in the fullfield
    name = words[-1]
    suffix = readaftersubstring("<", name)
    generictype = readbeforesubstring(">", suffix, backwards=True)
    return generictype


@lru_cache(maxsize=1, typed=True)
def dumpcsobject_field_getdatatype(fullfield: str) -> str:
    # Not Done
    fielddeclarationline = fullfield.strip()
    prefix = readbeforesubstring(";", fielddeclarationline)
    if dumpcsobject_field_hasdefault(fullfield):
        prefix = readbeforesubstring(" = ", prefix)
    # The data type is everything but the last word (which is the field name)
    words = getwords(prefix)
    assert len(words) > 1
    del words[-1]
    # Concatenate the words back into a string
    datatype = wordstostring(words)
    return datatype


def dumpcsobject_field_isdynamic(fullfield: str) -> bool:
    # Not Done
    datatype = dumpcsobject_field_getdatatype(fullfield)
    words = getwords(datatype)
    assert words
    return "dynamic" in words


def dumpcsobject_field_hasoffset(fullfield: str) -> bool:
    # Not Done
    fielddeclarationline = fullfield.strip()
    suffix = readaftersubstring(";", fielddeclarationline, backwards=True)
    return "// " in suffix


def dumpcsobject_field_getoffset(fullfield: str) -> str:
    # Not Done
    if not dumpcsobject_field_hasoffset(fullfield):
        # No offset
        return None
    fielddeclarationline = fullfield.strip()
    suffix = readaftersubstring(";", fielddeclarationline, backwards=True)
    offset = readaftersubstring("// ", suffix)
    return offset


def dumpcsobject_field_hasdefault(fullfield: str) -> bool:
    # Not Done
    # the " = " always comes before the default value,
    # so we do not have to worry if the default value is a string containing " = "
    return " = " in fullfield


def dumpcsobject_field_getdefault(fullfield: str) -> str:
    # Not Done
    if not dumpcsobject_field_hasdefault(fullfield):
        # No default
        return None
    fielddeclarationline = fullfield.strip()
    prefix = readbeforesubstring(";", fielddeclarationline, backwards=True)
    assert " = " in prefix
    # the " = " always comes before the default value,
    # so we do not have to worry if the default value is a string containing " = "
    default = readaftersubstring(" = ", prefix)
    return default


def dumpcsobject_getproperties(fullobject: str) -> list[dict]:
    # Not Done
    """

    Possible Improvements:

    Gets a list of properties from a dumpcs object

    fullobject: the content of the dumpcs object

    Return:
        list of properties in the dumpcs object
    """
    # Get the properties section of the dumpcs object
    if not dumpcsobject_hasproperties(fullobject):
        # No Properties
        return []
    suffix = readaftersubstring("\n\t// Properties", fullobject)
    checks = ("\n\t// Methods", "\n\t// Fields")
    found = False
    for check in checks:
        if check in suffix:
            propertiessection = readbeforesubstring(f"\n{check}", suffix)
            found = True
            break
    if not found:
        propertiessection = readbeforesubstring("\n}", suffix, backwards=True)
    propertydelimiter = "\n"
    # Split properties by "\n", which can be used to mark the start of each property
    fullproperties = propertiessection.split(propertydelimiter)
    if not fullproperties:
        return []
    # The split function will capture everything before the first property
    # since we split by the delimiter that starts properties, so delete that
    del fullproperties[0]
    # Build dictionary of properties from full properties
    properties = []
    for fullproperty in fullproperties:
        name = dumpcsobject_property_getname(fullproperty)
        datatype = dumpcsobject_property_getdatatype(fullproperty)
        basedatatype = datatype_getbase(datatype)
        isoverride = dumpcsobject_property_isoverride(fullproperty)
        isvirtual = dumpcsobject_property_isvirtual(fullproperty)
        hasgenericdatatype = dumpcsobject_property_hasgenericdatatype(fullproperty)
        if hasgenericdatatype:
            genericdatatype = dumpcsobject_property_getgenericdatatype(fullproperty)
        else:
            genericdatatype = None
        hasgetter = dumpcsobject_property_hasgetter(fullproperty)
        hassetter = dumpcsobject_property_hassetter(fullproperty)
        # The name Property is capitalized because property" is a keyword in python
        Property = {
            "content": fullproperty,
            "name": name,
            "datatype": datatype,
            "basedatatype": basedatatype,
            "isvirtual": isvirtual,
            "isoverride": isoverride,
            "hasgenericdatatype": hasgenericdatatype,
            "genericdatatype": genericdatatype,
            "hasgetter": hasgetter,
            "hassetter": hassetter,
        }
        properties.append(Property)
    return properties


def dumpcsobject_property_getname(fullproperty: str) -> str:
    # Not Done
    propertydeclarationline = fullproperty.strip()
    prefix = readbeforesubstring(" {", propertydeclarationline)
    words = getwords(prefix)
    assert len(words) > 1
    # The name of the property is the last word before the delimiter in the fullproperty
    lastword = words[-1]
    if dumpcsobject_property_hasgenericdatatype(fullproperty):
        assert "<" in lastword
        prefix = readbeforesubstring("<", lastword)
        assert ">" in lastword
        suffix = readaftersubstring(">", lastword, backwards=True)
        name = prefix + suffix
    else:
        name = lastword
    return name


def dumpcsobject_property_hasgenericdatatype(fullproperty: str) -> str:
    # Not Done
    propertydeclarationline = fullproperty.strip()
    prefix = readbeforesubstring(" {", propertydeclarationline)
    words = getwords(prefix)
    assert len(words) > 1
    return "<" in words[-1]

def dumpcsobject_property_getgenericdatatype(fullproperty: str) -> str:
    # Not Done
    if not dumpcsobject_property_hasgenericdatatype(fullproperty):
        # No generic type
        return None
    propertydeclarationline = fullproperty.strip()
    prefix = readbeforesubstring(" {", propertydeclarationline)
    words = getwords(prefix)
    assert len(words) > 1
    # The name of the property is the last word before the delimiter in the fullproperty
    lastword = words[-1]
    suffix = readaftersubstring("<", lastword)
    generictype = readbeforesubstring(">", suffix, backwards=True)
    return generictype


@lru_cache(maxsize=1, typed=True)
def dumpcsobject_property_getdatatype(fullproperty: str) -> str:
    # Not Done
    propertydeclarationline = fullproperty.strip()
    prefix = readbeforesubstring(" {", propertydeclarationline)
    # The data type is everything but the last word (which is the property name)
    words = getwords(prefix)
    assert len(words) > 1
    del words[-1]
    # Concatenate the words back into a string
    datatype = wordstostring(words)
    return datatype


def dumpcsobject_property_isvirtual(fullproperty: str) -> bool:
    # Not Done
    datatype = dumpcsobject_property_getdatatype(fullproperty)
    words = getwords(datatype)
    assert words
    return "virtual" in words


def dumpcsobject_property_isoverride(fullproperty: str) -> bool:
    # Not Done
    datatype = dumpcsobject_property_getdatatype(fullproperty)
    words = getwords(datatype)
    assert words
    return "override" in words


def dumpcsobject_property_getpropertymethods(fullproperty: str) -> str:
    propertydeclarationline = fullproperty.strip()
    suffix = readaftersubstring(" { ", propertydeclarationline)
    propertymethodssection = readbeforesubstring(" }", suffix, backwards=True)
    propertymethods = [propertymethod.strip() for propertymethod in propertymethodssection.split(";")]
    # The split function will capture everything after the last property
    # since we split by the delimiter that ends properties,
    # so delete that
    del propertymethods[-1]
    return propertymethods


def dumpcsobject_property_hasgetter(fullproperty: str) -> bool:
    # Not Done
    propertymethods = dumpcsobject_property_getpropertymethods(fullproperty)
    return "get" in propertymethods

def dumpcsobject_property_hassetter(fullproperty: str) -> bool:
    # Not Done
    propertymethods = dumpcsobject_property_getpropertymethods(fullproperty)
    return "set" in propertymethods


def dumpcs_getobjects(dumpcs: str,
                      objecttypefilter: Optional[set[str]]=None,
                      namespacefilter: Optional[set[str]]=None,
                      customfilter: Optional[Callable]=None,
                      makeobjectpaths=False,
                      getmethodhex=True,
                      libfilepath=None) -> list[dict]:
    #Not Done
    """
    Docs Not Done!
    Possible Improvements:
        1. Creating a new list is inefficient, modifying existing list would be ideal
        2. Directly using dumpcs.split() instead of using fullobjects variable may be faster,
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
        9. Supplying content and objectcache parameters to all functions, whether they use them or not,
        is good for consistency, readability, and refactoring, but sacrifices speed and memory

    Parses dumpcs file into a list of objects
    Does not remove blank lines

    Arguments:
        dumpcs: the contents of the dumpcs file
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
    fullobjects = dumpcs.split(f"\n{objectdelimiter}")
    #if not fullobjects:
    #    # If there aren't any objects in dumpcs (this is impossible, but just theoretically),
    #    # we can terminate the function now
    #    return []
    if not fullobjects:
        # exceptions.errors.unexpecteddumpcsformat(f"Error go brrrr")
        raise UnexpectedDumpcsFormatError("No objects in dumpcs", dumpcs)
    # The split function will capture everything before the first object
    # since we split by the delimiter that starts objects, so delete that
    del fullobjects[0]
    # Build dictionary of objects from full objects
    objects = []
    for fullobject in fullobjects:
        # Add "// Namespace: " back on, as string.split excludes the delimiter
        fullobject = objectdelimiter + fullobject
        hasnamespace = dumpcsobject_hasnamespace(fullobject)
        if hasnamespace:
            namespace = dumpcsobject_getnamespace(fullobject)
        else:
            namespace = None
        if namespacefilter and not(namespace in namespacefilter):
            continue
        # The name objecttype is used because "type" is a keyword
        objecttype = dumpcsobject_gettype(fullobject)
        if objecttypefilter and not (objecttype in objecttypefilter):
            continue
        isinherited = dumpcsobject_isinherited(fullobject)
        name = dumpcsobject_getname(fullobject, includenesting=False)
        isnested = dumpcsobject_isnested(fullobject)
        nesting = dumpcsobject_getnesting(fullobject, includename=False, innertoouter=True)
        datatype = dumpcsobject_getdatatype(fullobject)
        if isinherited:
            base = dumpcsobject_getbase(fullobject)
        else:
            base = None
        isgeneric = dumpcsobject_isgeneric(fullobject)
        if isgeneric:
            genericdatatype = dumpcsobject_getgenericdatatype(fullobject)
        else:
            genericdatatype = None
        # If a generic object is inherited from a base object that is also generic,
        # the base class's generic data type will always be the same as
        # the derived object's generic data type. So, there is no need to find / process
        # the base class's generic data type.
        typedefindex = dumpcsobject_gettypedefindex(fullobject)
        hasmethods = dumpcsobject_hasmethods(fullobject)
        if hasmethods:
            methods = dumpcsobject_getmethods(fullobject)
            hasconstructor = dumpcsobject_hasconstructor(fullobject)
            hasstaticconstructor = dumpcsobject_hasstaticconstructor(fullobject)
            updatetypes = dumpcsobject_getupdatetypes(fullobject)
        else:
            #methods = None
            methods = []
            hasconstructor = False
            hasstaticconstructor = False
            updatetypes = []
        hasfields = dumpcsobject_hasfields(fullobject)
        if hasfields:
            fields = dumpcsobject_getfields(fullobject)
        else:
            # fields = None
            fields = []
        hasproperties = dumpcsobject_hasproperties(fullobject)
        if hasproperties:
            properties = dumpcsobject_getproperties(fullobject)
        else:
            # properties = None
            properties = []
        #The name Object is capitalized because "object" is a keyword
        Object = {
            "content": fullobject,
            "name": name,
            "typedefindex": typedefindex,
            "type": objecttype,
            "hasnamespace": hasnamespace,
            "namespace": namespace,
            "datatype": datatype,
            "isinherited": isinherited,
            "base": base,
            "isnested": isnested,
            "nesting": nesting,
            "isgeneric": isgeneric,
            "genericdatatype": genericdatatype,
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
            path = dumpcsobject_getpath(fullobject)
            Object["path"] = path
        # Now that we have all the object's data, we can check against custom filter.
        if customfilter and not(customfilter(Object)):
            continue
        objects.append(Object)
    return objects


def dumpcs_getimages(dumpcs: str) -> list[dict]:
    #Not Done
    """
    Docs Not Done!
    Possible Improvements:
    """
    raise NotImplementedError("dumpcs_getimages function does not exist")


dumpcspath, encoding = r"C:\Users\zachy\OneDrive\Documents\Work\Projects\Polywar\64bit\dump.cs", 'utf8'
#dumpcspath, encoding = r"C:\Users\zachy\OneDrive\Documents\Work\Projects\Pixel Gun
# 3D\Pixel Gun 3D
# 16.6.1\Pixel Gun
# 3D 16.6.1 dump.cs", 'utf8'
outputpath = r"C:\Users\zachy\OneDrive\Documents\Work\Temp\Python Temps\parseddumpcs.json"
if __name__ == "__main__":
    with open(dumpcspath,encoding = encoding) as f:
        objects = dumpcs_getobjects(dumpcs_removeattributes(f.read()), makeobjectpaths=True, getmethodhex=False)
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