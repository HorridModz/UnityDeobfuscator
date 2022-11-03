from typing import Callable, Iterator, Union, Optional
import string
import copy

def removesubstring(s: str,sub: str) -> str:
    return(s.replace(sub,""))

def removesubstrings(s: str,subs: list[str]) -> str:
    for sub in subs:
        s = removesubstring(s,sub)
    return(s)

def removeallwhitespace(s: str) -> str:
    """Removes all whitespaces from a string, doesn't just trim leading and trailing"""
    _whitespace = [*string.whitespace]
    return(removesubstrings(s,_whitespace))

def iswhitespace(s: str) -> str:
    for thisletter in s:
        if not(thisletter.isspace()):
            return(False)
    return(True)

def trim(s: str,leading=True, trailing=True) -> str:
    if leading and trailing:
        return s.strip()
    elif leading:
        return s.lstrip()
    elif trailing:
        return s.rstrip()
    else:
        return s

def getlines(s: str,toremoveblanklines=False,totrimlines=False) -> list[str]:
    """
    1. Creating a new list is inefficient, modifying existing list would be ideal
    2. Directly using s.splitlines() instead of using lines variable may be faster, but sacrifices readability
    """
    lines = s.splitlines()
    newlines = []
    for line in lines:
        if totrimlines:
            line = trim(line, True, True) #No option for controlling trim options, just tzrim leading and trailing by default
        if not (iswhitespace(line) and toremoveblanklines):
            newlines.append(line)
    return(newlines)

def dumpcs_isvalid(dumpcs: str) -> bool:
    """
    Bad detection, needs proper algorithm
    """
    return "// Image" in dumpcs and "// RVA: 0x" in dumpcs and "// Namespace:" in dumpcs and " TypeDefIndex: " in dumpcs

def dumpcs_checkformat(dumpcs: str) -> list[str]:
    """
    Check for errors in dump.cs format
    Returns list of unexpected formats
    """

def dumpcs_hasattributes(dumpcs: str):
    return None


def dumpcs_constructor(path: str,attributeswarning=False) -> str:
    """
    #dumpcs = filemanager.read_file(path)
    #if not(dumpcs_isvalid):
        #exceptions.warnings.invaliddumpcs(path)
    #if attributeswarning and dumpcs_hasattributes:
        #exceptions.warnings.dumpcsattributeswarning(path)
    #return dumpcs
    """
    pass

def removeattributes(thisobject: str,toremovenewlines = False) -> str:
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