from typing import *
import string
import copy

def removesubstring(s: str,sub: str) -> str:
    #Done
    """
    Possible Improvements:

    Remove one substring from a string

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
    return(s.replace(sub,""))

def removesubstrings(s: str,subs: list[str]) -> str:
    #Done
    """
    Possible Improvements:

    Remove multiple substring from a string, in order of list

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
        s = removesubstring(s,sub)
    return(s)

def removeallwhitespace(s: str) -> str:
    #Done, but maybe could be optimized
    #NOTE: Function is named removeallwhitespace because old function removewhitespace
    #was for trimming. Once all functions use trim instead, this function can be renamed
    #back to removewhitespace.
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
    _whitespace = [*string.whitespace] #Should have a constant instead of unpacking string.whitespace eacch time
    return(removesubstrings(s,_whitespace))

def iswhitespace(s: str) -> bool:
    #Done
    """
    Possible Improvements:

    Detects if a string is all whitespace
    Works on strings with any length, including 0

    Example:
        String: "
             "
        Return: true

        String: "   hello world!
            hi"
        Return: false

    Arguments:
        s: string to check for whitespace

    Return:
        bool whether string is all whitespace
    """
    for letter in s:
        #Check whether each letter in the string is not whitespace
        if not(letter.isspace()):
            #Letter is not whitespace
            return(False)
    #All letters are whitespace
    return(True)

def trim(s: str,leading=True, trailing=True) -> str:
    #Done
    """
    Possible Improvements:

    Trims whitespace from a string

    Example:
        String: "   hello world!
        "
        Leading: true
        Trailing: true
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

def getlines(s: str,toremoveblanklines=False,totrimlines=False) -> list[str]:
    # Done, but maybe could be optimized
    """
    Possible Improvements:
        1. Creating a new list is inefficient, modifying existing list would be ideal
        2. Directly using s.splitlines() instead of using lines variable may be faster, but sacrifices readability

    Splits a string into a list of lines

    Example:
        String: "a
                    b

                 c  "
        toremoveblanklines: true
        totrimlines: true
        Return: ["a","b","c"]

    Arguments:
        s: string to split into lines
        toremoveblanklines: whether to ignore blank lines
        totrimlines: whether to trim leading and trailing whitespace
        (only leadhing / only trailing whitespace is not supported)

    Return:
        list of the string's lines
    """
    lines = s.splitlines()
    newlines = []
    for line in lines:
        if totrimlines:
            line = trim(line, True, True)
        if not (iswhitespace(line) and toremoveblanklines):
            newlines.append(line)
    return(newlines)

def dumpcs_isvalid(dumpcs: str) -> bool:
    #Not done
    """
    Bad detection, needs proper algorithm

    Determines whether a dumpcs file is valid
    This function only performs a short check on the file as a whole. The dumpcs_checkformat function analyzes the whole thing and is very picky .
    All dumpcs files entered should be valid, but of course they must be checked.

    Arguments:
        dumpcs: the string of the dumpcs file

    Return:
        bool whether the dumpcs is valid
    """
    # return "// Image" in dumpcs and "// RVA: 0x" in dumpcs and "// Namespace:" in dumpcs and " TypeDefIndex: " in dumpcs
    raise NotImplementedError("Dumpcs_isvalid function needs improvement")
    if len(dumpcs) == 0:
        return(False)
    return(True)

def dumpcs_checkformat(dumpcs: str) -> list[str]:
    #Not done
    """
    Scan dump.cs for unexpected formatting
    Returns list of unexpected formatting errors

    Arguments:
        dumpcs: the string of the dumpcs file

    Return:
        List of errors with the line number and error
    """
    raise NotImplementedError("Dumpcs_checkformat function not completed")

def dumpcs_hasattributes(dumpcs: str) -> bool:
    #Not done
    """
    Bad detection, needs proper algorithm

    Determines whether a dumpcs file has attributes

    Arguments:
        dumpcs: the string of the dumpcs file

    Return:
        bool whether the dumpcs has attributes
    """
    raise NotImplementedError("Dumpcs_hasattributes function not completed")
    #return "[CompilerGeneratedAttribute]" in dumpcs


def dumpcs_constructor(path: str,attributeswarning=False) -> str:
    #Done
    """
    Possible Improvements:
        1. No need to warn about attributes as they should be removed automatically.
        However, I want to keep this code commented out and not delete it in case I
        change my mind later

    Loads and initializes a dumpcs file

    Arguments:
        path: the file path of the dumpcs file

    Returns:
        string containing the contents of the dump.cs file
    """
    try:
        #dumpcs = filehandler.read_file(path)
        raise NotImplementedError("Filehandler.read_file function does not exist")
    except Exception as exception:
        raise exception
    if not(dumpcs_isvalid(dumpcs)):
        #raise exceptions.errors.invaliddumpcs(path)
        raise NotImplementedError("Exceptions.errors.invaliddumpcs exception does not exist")
    #No need to warn about attributes as they should be removed automatically
    #if attributeswarning and dumpcs_hasattributes:
        #exceptions.warnings.dumpcsattributeswarning(path)
    formaterrors = dumpcs_checkformat(dumpcs)
    if formaterrors != []:
        #exceptions.warnings.unexpecteddumpcsformat(path,formaterrors)
        raise NotImplementedError("Exceptions.warnings.unexpecteddumpcsformat function does not exist")
    return dumpcs


def removeattributes(thisobject: str,toremovenewlines = False) -> str:
    # Not done
    """
    Possible Improvements:
        1. No need to warn about attributes as they should be removed automatically.
        However, I want to keep this code commented out and not delete it in case I
        change my mind later

    Loads and initializes a dumpcs file

    Arguments:
        path: the file path of the dumpcs file

    Returns:
        string containing the contents of the dump.cs file
   """
    if thisobject.attributesremoved:
        return(thisobject)
    #1. Creating a new list is inefficient, modifying existing list would be ideal
    #2. Directly using getlines() instead of using lines variable may be faster, but sacrifices readability
    lines = getlines(thisobject,False,False)
    newlines = []
    for thisline in lines:
            newline = removewhitespace(thisline,True,False,False)
            if ((letter(1,newline) == _attributestart) and (contains(_attributeend,newline))): #yes, purposely 1, not 0 - begins with tab (" [")
                if contains(_attributeend + " ",newline):
                    newline = readafter(newline,_attributeend + " ")
                else:
                    newline = readafter(newline,_attributeend)
                if (not(newline == "") and not((checkforstringat(" " + _isoffsetstring,newline,1)) or (checkforstringat(_isoffsetstring,newline,1)))): # rva is only after we remove compiler generated etc., so it is useless
                     newlines = listadd(newline,newlines)
            else:
                newline = thisline
                if not(toremovenewlines and (newline == "")):
                    newlines = listadd(newline,newlines)
    thisobject.attributesremoved = True
    return(linestostring(newlines))