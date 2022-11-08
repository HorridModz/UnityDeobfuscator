import sys
# noinspection PyUnresolvedReferences
import copy
from typing import *
import string
# noinspection PyUnresolvedReferences
from functools import *


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
    #Done
    """
    Docs Not Done!

    This function is based off of
    https://stackoverflow.com/questions/12572362/how-to-get-a-string-after-a-specific-substring/57064170#57064170
    Possible Improvements:
        1.  Directly returning instead of using suffix variable may be faster, but sacrifices
        readability and simplicity
    """
    if lengthwarning and len(sub) > len(s):
        raise SyntaxWarning(f"Call to readaftersubstring(sub={sub}, str={s}): \
         substring is longer than full string")
    prefix, success, suffix = s.partition(sub)
    if not success:
        suffix = prefix
    return suffix


def readbeforesubstring(sub: str, s: str, lengthwarning=True) -> str:
    #Done
    """
    Docs not done!

    This function is based off of
    https://stackoverflow.com/questions/12572362/how-to-get-a-string-after-a-specific-substring/57064170#57064170

    Possible Improvements:
        1.  Directly returning instead of using prefix variable may be faster, but sacrifices
        readability and simplicity
    """
    if lengthwarning and len(sub) > len(s):
        raise SyntaxWarning(f"Call to readaftersubstring(sub={sub}, str={s}): \
         substring is longer than full string")
    prefix, success, suffix = s.partition(sub)
    if not success:
        prefix = suffix
    return prefix


def removesubstring(sub: str, s: str) -> str:
    #Done
    """
    Possible Improvements:

    Removes one substring from a string

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
    #Done
    """
    Possible Improvements:

    Removes multiple substring from a string, in order of the list

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
    #Done
    """
    Doc Not Done
    """
    return s.replace(sub, replace)


def replacesubstrings(s: str, subs: list[str], replace: str) -> str:
    #Done
    """
    Doc Not Done
    """
    for sub in subs:
        s = replacesubstring(s, sub, replace)
    return s


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
    # Should have a constant instead of unpacking
    # string.whitespace each time
    _whitespace = [*string.whitespace]
    return removesubstrings(s, _whitespace)


def removeblanklines(s: str, toremovewhitespacelines=True) -> str:
    #Not Done
    """
    Possible Improvements:

    Removes all blank lines from a string

    Example:
        String: "
        blank
            lines will be

            removed from

            thisstr
         ing"
        toremovewhitespacelines: true
        Return: "blank
            lines will be
            removed from
            thisstr
         ing"

    Arguments:
        s: string to remove blank lines from
        toremovewhitespacelines: whether to remove lines with only whitespace (eg: "    ")

    Return:
        string with blank lines removed
    """
    if toremovewhitespacelines:
        raise NotImplementedError("removeblanklines with toremovewhitespacelines is not done")
    else:
        return replacesubstring(s, "\n\n", "\n")


def iswhitespace(s: str, totreatblankaswhitespace=True) -> bool:
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
        totreatblankaswhitespace: whether to treat "" as whitespace

    Return:
        bool whether string is all whitespace
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
    #Done
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
        string containing all the words concatenated by concatenator (default space)
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
    # Done, but maybe could be optimized
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
        string containing all the lines concatenated by new line
    """
    return wordstostring(lines, totrimlines, toignoreblanklines, toignoreblanklines, "\n")


def dumpcs_isvalid(dumpcs: str) -> bool:
    #Not done
    """
    Bad detection, needs proper algorithm

    Determines whether a dumpcs file is valid
    All dumpcs files entered should be valid, but of course they must be checked.
    Note: This function only performs a short check on the file as a whole.
    On the other hand, the dumpcs_checkformat function analyzes the whole thing and is very picky .

    Arguments:
        dumpcs: the string of the dumpcs file

    Return:
        bool whether the dumpcs is valid
    """
    # return "// Image" in dumpcs and "// RVA: 0x" in dumpcs and "// Namespace:" in dumpcs\
    # and " TypeDefIndex: " in dumpcs
    raise NotImplementedError("Dumpcs_isvalid function needs improvement")
    if len(dumpcs) == 0:
        return False
    return True


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


def dumpcs_constructor(path: str, attributeswarning=False) -> str:
    #Done, but needs improvement
    """
    Possible Improvements:
        1. No need to warn about attributes as they should be removed automatically.
        However, I want to keep this code commented out and not delete it in case I
        change my mind later.
        2. Setting dumpcs variable after removing attributes makes code more readable and concise,
        but is less inefficient than directing passing result of dumpcs_removeattributes.
        In addition, attributes must be removed *before* dumpcs is checked for format errors
        3. Does try except clause make a difference? IDK whether to keep it.

    Loads and initializes a dumpcs file

    Arguments:
        path: the file path of the dumpcs file
        attributeswarning: deprecated, please do not set to true!

    Returns:
        string containing the contents of the dump.cs file
    """
    #Does this try except clause make a difference? IDK whether to keep it
#    try:
#        dumpcs = filehandler.read_file(path)
#        raise NotImplementedError("filehandler.read_file function does not exist")
#    except Exception as exception:
#        raise exception
#    dumpcs = filehandler.read_file(path)
    raise NotImplementedError("filehandler.read_file function does not exist")
    if not(dumpcs_isvalid(dumpcs)):
        #raise exceptions.errors.invaliddumpcs(path)
        raise NotImplementedError("exceptions.errors.invaliddumpcs function does not exist")
    #No need to warn about attributes as they should be removed automatically
    #if attributeswarning and dumpcs_hasattributes(dumpcs):
        #exceptions.warnings.dumpcsattributeswarning(path)
    if dumpcs_hasattributes(dumpcs):
        dumpcs = dumpcs_removeattributes(dumpcs)
    formaterrors = dumpcs_checkformat(dumpcs)
    if formaterrors != []:
        #exceptions.warnings.unexpecteddumpcsformatearly(path,formaterrors)
        raise NotImplementedError("exceptions.warnings.unexpecteddumpcsformatearly function does not exist")
    return dumpcs


def dumpcs_removeattributes(dumpcs: str) -> str:
    #Not done
    """
    Possible Improvements:
        1. Creating a new list of lines is inefficient, modifying existing list would be ideal
        2. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity

    Removes attributes from a dumpcs file
    Does not process attributes, only removes them
    Does not remove blank lines yet

    Arguments:
        dumpcs: the string of the dumpcs file

    Returns:
        string containing dumpcs content with attributes removed
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


def dumpcsobject_getnamespace(content: str,
                              objectcache: dict[Any, Any],
                              namespacecache: dict[str] = {}) -> str:
    # Yes, the multiple default argument is intentional.
    # It allows us to cache namespaces within this function.
    # Not Done
    """
    Docs Not Done!
    Possible Improvements:
        1. Using string.find "\n" and taking a substring is faster than splitting the object into lines,
        but sacrifices readability and simplicity
        2. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity
        3.  Directly returning instead of using variable may be faster, but sacrifices
        readability and simplicity
        4. Directly using lines[0] instead of using namespaceline variable may be faster, but sacrifices
        readability and simplicity

    Gets the namespace of a dumpcs object
    """
    lines = objectcache["lines"]
    namespaceline = lines[0]
    if namespaceline == "// Namespace: ":
        namespace = ""
    else:
        if namespaceline in namespacecache:
            namespace = namespacecache[namespaceline]
        else:
            namespace = readaftersubstring("// Namespace: ", namespaceline)
            namespacecache[namespaceline] = namespace
    return namespace


def dumpcsobject_gettype(content, objectcache: dict[Any, Any]) -> str:
    # Not Done
    """
    Docs Not Done!
    Possible Improvements:
        1. Using string.find "\n" and taking a substring is faster than splitting the object into lines,
        but sacrifices readability and simplicity
        2. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity
        3.  Directly returning instead of using type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        4. Directly using lines[1] instead of using objectdeclarationline variable may be faster, but sacrifices
        readability and simplicity
        5. Object types should be a constant

    Gets the type (struct, class, enum, or interface) of a dumpcs object
    """
    objecttypes = {"class", "struct", "interface", "enum"}  # should be a constant!
    words = objectcache["objectdeclarationwords"]
    for word in words:
        if word in objecttypes:
            return word
    # Object type (class, struct, enum, interface) not found
    #exceptions.errors.unexpecteddumpcsformat(f"Could not find type of object:\n{content}")
    raise NotImplementedError("exceptions.errors.unexpecteddumpcsformat function does not exist")


def dumpcsobject_getdatatype(content, objectcache: dict[Any, Any]) -> str:
    # Not Done
    """
    Docs Not Done!
    Possible Improvements:
        1. Using string.find "\n" and taking a substring is faster than splitting the object into lines,
        but sacrifices readability and simplicity
        2. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity
        3.  Directly returning instead of using data type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        4. Directly using lines[1] instead of using objectdeclarationline variable may be faster, but sacrifices
        readability and simplicity
        5. Object types should be a constant
        6. Using a string for data type instead of using a list and concatenating it into a string may be faster,
        but sacrifices readability and simplicity

    Gets the data type of a dumpcs object
    """
    objecttypes = {"class", "struct", "interface", "enum"} # should be a constant!
    words = objectcache["objectdeclarationwords"]
    datatypewords = []
    for word in words:
        if word in objecttypes:
            datatype = wordstostring(datatypewords)
            return datatype
        else:
            datatypewords.append(word)
    # Object type (class, struct, enum, interface) not found
    #exceptions.errors.unexpecteddumpcsformat(f"Could not find type of object:\n{content}")
    raise NotImplementedError("exceptions.errors.unexpecteddumpcsformat function does not exist")


def dumpcsobject_getname(content, objectcache: dict[Any, Any]) -> str:
    # Not Done
    """
    Docs Not Done!
    Possible Improvements:
        1. Using string.find "\n" and taking a substring is faster than splitting the object into lines,
        but sacrifices readability and simplicity
        2. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity
        3.  Directly returning instead of using data type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        4. Directly using lines[1] instead of using objectdeclarationline variable may be faster, but sacrifices
        readability and simplicity
        5. Object types should be a constant
        6. Using a string for data type instead of using a list and concatenating it into a string may be faster,
        but sacrifices readability and simplicity

    Gets the data type of a dumpcs object
    """
    objectdeclarationline = objectcache["objectdeclarationline"]
    if objectcache["isinherited"]:
        prefix = readbeforesubstring(" : ", objectdeclarationline)
    else:
        prefix = readbeforesubstring(" //", objectdeclarationline)
    words = getwords(prefix)
    name = words[len(words) - 1]
    return name


def dumpcsobject_getbase(content, objectcache: dict[Any, Any]) -> Union[str, None]:
    # Not Done
    """
    Docs Not Done!
    Possible Improvements:
        1. Using string.find "\n" and taking a substring is faster than splitting the object into lines,
        but sacrifices readability and simplicity
        2. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity
        3.  Directly returning instead of using data type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        4. Directly using lines[1] instead of using objectdeclarationline variable may be faster, but sacrifices
        readability and simplicity
        5. Object types should be a constant
        6. Using a string for data type instead of using a list and concatenating it into a string may be faster,
        but sacrifices readability and simplicity

    Gets the data type of a dumpcs object
    """
    objectdeclarationline = objectcache["objectdeclarationline"]
    if not(objectcache["isinherited"]):
        return None
    suffix = readaftersubstring(" : ", objectdeclarationline)
    base = readbeforesubstring(" //", suffix)
    return base


def dumpcsobject_gettypedefindex(content, objectcache: dict[Any, Any]) -> str:
    # Not Done
    """
    Docs Not Done!
    Possible Improvements:
        1. Using string.find "\n" and taking a substring is faster than splitting the object into lines,
        but sacrifices readability and simplicity
        2. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity
        3.  Directly returning instead of using data type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        4. Directly using lines[1] instead of using objectdeclarationline variable may be faster, but sacrifices
        readability and simplicity
        5. Object types should be a constant
        6. Using a string for data type instead of using a list and concatenating it into a string may be faster,
        but sacrifices readability and simplicity

    Gets the data type of a dumpcs object
    """
    objectdeclarationline = objectcache["objectdeclarationline"]
    typedefindex = readaftersubstring("// TypeDefIndex: ", objectdeclarationline)
    return typedefindex


def dumpcsobject_isinherited(content, objectcache: dict[Any, Any]) -> bool:
    # Not Done
    """
    Docs Not Done!
    Possible Improvements:
        1. Using string.find "\n" and taking a substring is faster than splitting the object into lines,
        but sacrifices readability and simplicity
        2. Directly using getlines() instead of using lines variable may be faster, but sacrifices
        readability and simplicity
        3.  Directly returning instead of using data type variable and breaking loop out of loop may be faster,
        but sacrifices readability and simplicity
        4. Directly using lines[1] instead of using objectdeclarationline variable may be faster, but sacrifices
        readability and simplicity
        5. Object types should be a constant
        6. Using a string for data type instead of using a list and concatenating it into a string may be faster,
        but sacrifices readability and simplicity

    Gets the data type of a dumpcs object
    """
    objectdeclarationline = objectcache["objectdeclarationline"]
    return " : " in objectdeclarationline


def dumpcs_getobjects(dumpcs: str,
                      createtypemodels=True,
                      objecttypefilter: Union[set[str], None] = None,
                      namespacefilter: Union[set[str], None] = None,
                      customfilter: Union[Callable, None] = None) -> list[dict]:
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
        5. To save memory and speed, maybe only add object base if it exists. However, this
        sacrifices readability and simplicity
        6. Setting object's type model to None decreases errors and complexity, but
        takes up extra memory and sacrifices speed
        7. Returning a dictionary of objects by path (namespace -> object) may be faster and simpler than
        returning a list of dictionaries (as to grab an object out of the list by its path, the list must be
        iterated through until a match is found), but a list is simpler, easier, and faster to create,
        process, and iterate over
        8. Object delimiter should be a constant

    Parses dumpcs file into a list of objects
    Does not remove blank lines
    """
    objectdelimiter = "// Namespace: "  # Should be a constant
    if dumpcs_hasattributes(dumpcs):
        #exceptions.warnings.dumpcsattributesnotremoved()
        raise NotImplementedError("exceptions.warnings.dumpcsattributesnotremoved function does not exist")
        dumpcs = dumpcs_removeattributes(dumpcs)
    # Split dumpcs by "// Namespace: ", which can be used to mark the start of each object
    fullobjects = dumpcs.split(objectdelimiter)
    if fullobjects == []:
        # If there aren't any objects in dumpcs (this is impossible, but just theoretically),
        # we can terminate the function now to keep it simple
        return []
    # The split function will capture everything before the first object
    # since we split by the delimiter that starts objects, so delete that
    del fullobjects[0]
    # Build dictionary of objects from full objects
    objects = []
    for fullobject in fullobjects:
        # Create a cache of repetitive function calls so we only have to calculate them once
        objectcache = {}
        # Add "// Namespace: " back on, as string.split excludes the delimiter
        content = objectdelimiter + fullobject
        lines = getlines(content)
        objectcache["lines"] = lines
        # We only need lines cached to calculate namespace
        namespace = dumpcsobject_getnamespace(content, objectcache)
        # Exit early on namespacefilter to save some work
        if namespacefilter is not None and not(namespace in namespacefilter):
            continue
        objectdeclarationline = lines[1]
        objectcache["objectdeclarationline"] = objectdeclarationline
        objectcache["objectdeclarationwords"] = getwords(objectdeclarationline)
        # The name objecttype is used because type is a keyword
        objecttype = dumpcsobject_gettype(content, objectcache)
        # Exit early on objecttypefilter to save some work
        if objecttypefilter is not None and not (objecttype in objecttypefilter):
            continue
        isinherited = dumpcsobject_isinherited(content, objectcache)
        objectcache["isinherited"] = isinherited
        name = dumpcsobject_getname(content, objectcache)
        datatype = dumpcsobject_getdatatype(content, objectcache)
        if isinherited:
            base = dumpcsobject_getbase(content, objectcache)
        else:
            base = None
        typedefindex = dumpcsobject_gettypedefindex(content, objectcache)
        methods = dumpcsobject_getmethods(content, objectcache)
        fields = dumpcsobject_getfields(content, objectcache)
        properties = dumpcsobject_getproperties(content, objectcache)
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
        # This allows us to avoid creating the object's type model if the object is going to be ignored
        if customfilter is not None and not(customfilter(Object)):
            continue
        if createtypemodels:
            # Create type model from the object's data, then add it to the object
            typemodel = buildtypemodel(Object)
            Object["typemodel"] = typemodel
        else:
            Object["typemodel"] = None
        objects.append(Object)
    return objects
