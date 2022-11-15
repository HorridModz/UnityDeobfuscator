import sys
# noinspection PyUnresolvedReferences
import copy
from typing import *
import string
# noinspection PyUnresolvedReferences


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


def readaftersubstring(sub: str, s: str, lengthwarning=True) -> str:
    # Done
    """
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
        raise SyntaxWarning(f"Call to readaftersubstring(sub={sub}, str={s}): \
         substring is longer than full string")
    prefix, found, suffix = s.partition(sub)
    if not found:
        suffix = prefix
    return suffix


def readbeforesubstring(sub: str, s: str, lengthwarning=True) -> str:
    # Done
    """
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
        raise SyntaxWarning(f"Call to readaftersubstring(sub={sub}, str={s}): \
         substring is longer than full string")
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
        Return: true

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
        if totreatblankaswhitespace:
            return True
        else:
            return False
    else:
        return s.isspace()


def trim(s: str, leading=True, trailing=True) -> str:
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
        toremoveblanklines: true
        totrimlines: true
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
                  totrimlines=True,
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
        dumpcs: the string of the dumpcs file

    Return:
        whether the dumpcs is valid
    """
    checks = ("// Image 0:", "// Namespace:", "class", "	// Methods", "// RVA: 0x")
    for check in checks:
        if check not in dumpcs:
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
        list of errors with the line number and error
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
        dumpcs: the string of the dumpcs file
        fastcheck: whether to perform a fast or through check for attributes (fast should be sufficient,
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
            if trimmedline == "" or trimmedline[0] != "[":
                return True
        return False


def dumpcs_constructor(path: str, attributeswarning=False) -> str:
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
        attributeswarning: deprecated, please do not set to true!

    Return:
        the contents of the dump.cs file
    """
    # filehandler.read_file may throw an exception, if this happens we
    # let it get passed on to the the caller of this function
#   dumpcs = filehandler.read_file(path)
    raise NotImplementedError("filehandler.read_file function does not exist")
    if not(dumpcs_isvalid(dumpcs)):
        #raise exceptions.errors.invaliddumpcs(path)
        raise NotImplementedError("exceptions.errors.invaliddumpcs function does not exist")
    if dumpcs_hasattributes(dumpcs):
        dumpcs = dumpcs_removeattributes(dumpcs)
    formaterrors = dumpcs_checkformat(dumpcs)
    if formaterrors != []:
        #exceptions.warnings.unexpecteddumpcsformatearly(path,formaterrors)
        raise NotImplementedError("exceptions.warnings.unexpecteddumpcsformatearly function does not exist")
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
        dumpcs: the string of the dumpcs file

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
    return linestostring(newlines)


def dumpcsobject_getnamespace(objectcache: dict[Any, Any],
                              namespacecache: dict[str] = {}) -> str:
    # Yes, the multiple default argument is intentional.
    # It allows us to cache namespaces within this function.
    # Done
    """

    Possible Improvements:
        1.  Directly returning instead of using variable may be faster, but sacrifices
        readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets the namespace of a dumpcs object
    Uses a dictionary to cache the result

    Example:
        objectcache.namespaceline: // Namespace: Microsoft.Win32
        Return: Microsoft.Win32


    Arguments:
        objectcache: dictionary of cached object data for the function to use. Must contain the namespaceline
        of dumpcs.
        namespacecache: a dictionary used by the function to cache the result of namespaces. This default
        argument is mutable to allow for an easy way to store information between function calls. Should not
        be specified by the caller

    Return:
        namespace of the dumpcs sobject
    """
    # Everything after "// Namespace: " in the namespaceline is the object's namespace
    namespacedelimiter = "// Namespace: "
    namespaceline = objectcache["namespaceline"]
    if namespaceline == namespacedelimiter:
        namespace = ""
    else:
        if namespaceline in namespacecache:
            namespace = namespacecache[namespaceline]
        else:
            namespace = readaftersubstring(namespacedelimiter, namespaceline)
            namespacecache[namespaceline] = namespace
    return namespace


def dumpcsobject_gettype(objectcache: dict[Any, Any]) -> str:
    # Done
    """

    Possible Improvements:
        1.  Directly returning instead of using type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        2. Object types should be a constant
        3. IDK if using a dictionary cache is faster or ironically slower

    Gets the type (struct, class, enum, or interface) of a dumpcs object

    Example:
        objectcache.objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: class


    Arguments:
        objectcache: dictionary of cached object data for the function to use. Must contain the objectdeclarationline
        of dumpcs.

    Return:
        type of the dumpcs object
    """
    # Find the first word that is a valid type of object in the object declaration line
    # This is the type of the object
    objecttypes = {"class", "struct", "interface", "enum"}  # should be a constant!
    words = objectcache["objectdeclarationwords"]
    for word in words:
        if word in objecttypes:
            return word
    # Object type (class, struct, enum, interface) not found
    #exceptions.errors.unexpecteddumpcsformat(f"Could not find type of object:\n{objectcache["objectdeclarationwords"]}")
    raise NotImplementedError("exceptions.errors.unexpecteddumpcsformat function does not exist")


def dumpcsobject_getdatatype(objectcache: dict[Any, Any]) -> str:
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
        objectcache.objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: public static


    Arguments:
        objectcache: dictionary of cached object data for the function to use. Must contain the objectdeclarationline
        of dumpcs.

    Return:
        data type of the dumpcs object
    """
    # Find everything before the first word that is a valid type of object in the object declaration line
    # This is the data type of the object
    objecttypes = {"class", "struct", "interface", "enum"}  # should be a constant!
    words = objectcache["objectdeclarationwords"]
    datatypewords = []
    for word in words:
        if word in objecttypes:
            # Concatenate the words back into a string
            datatype = wordstostring(datatypewords)
            return datatype
        else:
            # Add this word onto the data type
            datatypewords.append(word)
    # Object type (class, struct, enum, interface) not found
    #exceptions.errors.unexpecteddumpcsformat(f"Could not find type of object:\n{objectcache["objectdeclarationwords"]}")
    raise NotImplementedError("exceptions.errors.unexpecteddumpcsformat function does not exist")


def dumpcsobject_getname(objectcache: dict[Any, Any]) -> str:
    # Done
    """

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets the name of a dumpcs object

    Example:
        objectcache.objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: Registry


    Arguments:
        objectcache: dictionary of cached object data for the function to use. Must contain the objectdeclarationline
        of dumpcs.

    Return:
        name of the dumpcs object
    """
    objectdeclarationline = objectcache["objectdeclarationline"]
    if objectcache["isinherited"]:
        # If the object is inherited, just return the name of the derived object
        prefix = readbeforesubstring(" : ", objectdeclarationline)
    else:
        prefix = readbeforesubstring(" //", objectdeclarationline)
    # The name of the object is the last word before the delimiter in the objectdeclarationline
    words = getwords(prefix)
    name = words[len(words) - 1]
    return name


def dumpcsobject_getbase(objectcache: dict[Any, Any]) -> Optional[str]:
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
        objectcache.objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: None

        objectcache.objectdeclarationline: public class DecalsMeshRenderer : MonoBehaviour // TypeDefIndex: 4727
        Return: MonoBehavior


    Arguments:
        objectcache: dictionary of cached object data for the function to use. Must contain the objectdeclarationline
        of dumpcs.

    Returns:
        base class of the dumpcs object, or None if the dumpcs object is not inherited
    """
    objectdeclarationline = objectcache["objectdeclarationline"]
    if not(objectcache["isinherited"]):
        return None
    suffix = readaftersubstring(" : ", objectdeclarationline)
    base = readbeforesubstring(" //", suffix)
    return base


def dumpcsobject_gettypedefindex(objectcache: dict[Any, Any]) -> str:
    # Done
    """

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets the typedefindex of a dumpcs object

    Example:
        objectcache.objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: 4

    Arguments:
        objectcache: dictionary of cached object data for the function to use. Must contain the objectdeclarationline
        of dumpcs.

    Return:
        typedefindex of the dumpcs object
    """
    objectdeclarationline = objectcache["objectdeclarationline"]
    typedefindex = readaftersubstring("// TypeDefIndex: ", objectdeclarationline)
    return typedefindex


def dumpcsobject_isinherited(objectcache: dict[Any, Any]) -> bool:
    # Not Done
    """

    Possible Improvements:
        1. Directly returning instead of using variable may be faster,
        but sacrifices readability and simplicity
        2. IDK if using a dictionary cache is faster or ironically slower

    Gets whether a dumpcs object is inherited

    Examples:
        objectcache.objectdeclarationline: public static class Registry // TypeDefIndex: 4
        Return: False

        objectcache.objectdeclarationline: public class DecalsMeshRenderer : MonoBehaviour // TypeDefIndex: 4727
        Return: True

    Arguments:
        objectcache: dictionary of cached object data for the function to use. Must contain the objectdeclarationline
        of dumpcs.

    Return:
        whether the dumpcs object is inherited
    """
    objectdeclarationline = objectcache["objectdeclarationline"]
    return " : " in objectdeclarationline


def dumpcs_getobjects(dumpcs: str,
                      createtypemodels=True,
                      objecttypefilter: Optional[set[str]] = None,
                      namespacefilter: Optional[set[str]] = None,
                      customfilter: Optional[Callable] = None) -> list[dict]:
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
        namespacefilter: filter to only process objects that are in certain namespaces
        (set to None to disable filter)
        customfilter: filter that is supplied the finished object dictionary and tells the function to only
        process objects that satisfy custom conditions (set to None to disable filter)

    Return:
        list of parsed objects from the dumpcs file
    """
    objectdelimiter = "// Namespace: "  # Should be a constant
    if dumpcs_hasattributes(dumpcs):
        exceptions.warnings.dumpcsattributesnotremoved()
        raise NotImplementedError("exceptions.warnings.dumpcsattributesnotremoved function does not exist")
        dumpcs = dumpcs_removeattributes(dumpcs)
    # Split dumpcs by "// Namespace: ", which can be used to mark the start of each object
    fullobjects = dumpcs.split(objectdelimiter)
    if fullobjects == []:
        # If there aren't any objects in dumpcs (this is impossible, but just theoretically),
        # we can terminate the function now
        return []
    # The split function will capture everything before the first object
    # since we split by the delimiter that starts objects, so delete that
    del fullobjects[0]
    # Build dictionary of objects from full objects
    objects = []
    for fullobject in fullobjects:
        # Create a cache of repetitive function calls so we only have to do them once
        objectcache = {}
        # Add "// Namespace: " back on, as string.split excludes the delimiter
        content = objectdelimiter + fullobject
        lines = getlines(content)
        objectcache["lines"] = lines
        namespaceline = lines[0]
        objectcache["namespaceline"] = namespaceline
        # We only need namespaceline cached to find the object's namespace
        namespace = dumpcsobject_getnamespace(objectcache)
        # Exit early on namespacefilter to save some work
        if namespacefilter is not None and not(namespace in namespacefilter):
            continue
        objectdeclarationline = lines[1]
        objectcache["objectdeclarationline"] = objectdeclarationline
        objectcache["objectdeclarationwords"] = getwords(objectdeclarationline)
        # The name objecttype is used because type is a keyword
        objecttype = dumpcsobject_gettype(objectcache)
        # Exit early on objecttypefilter to save some work
        if objecttypefilter is not None and not (objecttype in objecttypefilter):
            continue
        isinherited = dumpcsobject_isinherited(objectcache)
        objectcache["isinherited"] = isinherited
        name = dumpcsobject_getname(objectcache)
        datatype = dumpcsobject_getdatatype(objectcache)
        if isinherited:
            base = dumpcsobject_getbase(objectcache)
        else:
            base = None
        typedefindex = dumpcsobject_gettypedefindex(objectcache)
        methods = dumpcsobject_getmethods(objectcache)
        fields = dumpcsobject_getfields(objectcache)
        properties = dumpcsobject_getproperties(objectcache)
        #The name Object is capitalized because object is a keyword in python
        Object = {
            "content": content,
            "name": name,
            "typedefindex": typedefindex,
            "type": objecttype,
            "namespace": namespace,
            "datatype": datatype,
            "isinherited": isinherited,
            "methods": methods,
            "fields": fields,
            "properties": properties,
            "base": base,
        }
        # Now that we have all the object's data, we can check against custom filter.
        if customfilter is not None and not(customfilter(Object)):
            continue
        if createtypemodels:
            # Create type model from the object's data, then append the type model to the object's data
            typemodel = buildtypemodel(Object)
            Object["typemodel"] = typemodel
        else:
            Object["typemodel"] = None
        objects.append(Object)
    return objects
