def loaddumpcs(path,attributeswarning = True):
    global dumpcs
    dumpcs = read_file(path)
    if not("// Image" in dumpcs and "// RVA: 0x" in dumpcs and "// Namespace:" in dumpcs and " TypeDefIndex: " in dumpcs):
        invaliddumpcswarning(path)
    #if (attributeswarning and (contains("[CompilerGeneratedAttribute]",dumpcs))): #and (contains("[DebuggerBrowsableAttribute]",dumpcs))):
        #dumpcsattributeswarning(path)
    return(dumpcs)

def getobjectof(index):
    index = int(index)
    if not(variableexists("dumpcs")):
        objectnotdeclarederror("dumpcs")
        return(None)
    if index > (len(dumpcs)- len("// Namespace: ")): #Impossible scenario, but ocd makes me put this here!
        return("")
    rangebehind = 0
    startpos = 0
    while startpos == 0:
        startpos = dumpcs.find("// Namespace: ",((index - rangebehind) - len("// Namespace: ")),(index - rangebehind)) + 1
        if (((index - rangebehind) - len("// Namespace: ")) < 1): #Not found - must be the beginning (shouldn't happen)
            startpos = 0
            return("") # no method
        rangebehind = rangebehind + 1
    endpos = dumpcs.find("// Namespace: ",startpos + len("// Namespace: "),len(dumpcs)) #find the next "Namespace: " after startpos
    if endpos == -1: #Not found - must be the last object
        endpos = len(dumpcs) #set to the end
    return (removeblanklines(substring(dumpcs,startpos,endpos),True,True)) #the object is between namespaces

def getmethodof(index):
    index = int(index)
    if not(variableexists("dumpcs")):
        objectnotdeclarederror("dumpcs")
        return(None)
    if index > (len(dumpcs)- len("\n\n")): #Impossible scenario, but ocd makes me put this here!
        return("")
    rangebehind = 0
    startpos = 0
    while startpos == 0:
        startpos = dumpcs.find("\n\n",((index - rangebehind) - len("\n\n")),(index - rangebehind)) + 1
        if (((index - rangebehind) - len("\n\n")) < 1): #Not found - must be the beginning (shouldn't happen)
            startpos = 0
            return("") # no method
        rangebehind = rangebehind + 1
    endpos = dumpcs.find("\n\n",startpos + len("\n\n"),len(dumpcs)) #find the next \n after startpos
    if endpos == -1: #Not found - shouldn't be possible but we assume it is end of dump.cs
        endpos = len(dumpcs) #set to the end
    methodline = removeblanklines(substring(dumpcs,startpos,endpos)).strip()
    if ((contains(_offsetsuffix,methodline)) and (len(getlines(methodline))) == 1): #just method offset line
        rangebehind = -1
        endpos = 1
        while endpos == 1:
            endpos = dumpcs.find("\n\n",startpos + 3,(startpos + ((index - rangebehind) + len("\n\n")))) + 2
            if  (((index - rangebehind) + len("\n\n")) > len(dumpcs)): #Not found - shouldn't be possible but we assume it is end of dump.cs
                endpos = len(dumpcs) #set to the end
            rangebehind = rangebehind - 1
        methodline = removeblanklines(substring(dumpcs,startpos,endpos)).strip()
        lines = getlines(methodline)
        lines[0] = lines[0].strip() #remove whitespace from the two lines
        lines[1] = lines[1].strip()
        methodline = linestostring(lines)
        if not((contains(_isoffsetstring,methodline)) and contains(_ismethodstring,methodline)): #It isn't a method
            return("")
        else:
            return(methodline)
    else: #method offset line and method type line, or not method
        lines = getlines(methodline)
        if len(getlines(methodline)) < 2: #error - must not be a method
            return("")
        lines[0] = lines[0].strip() #remove whitespace from the two lines
        lines[1] = lines[1].strip()
        methodline = linestostring(lines)
        if not(contains(_offsetsuffix,methodline)): #error - must not be a method
            return("")
        if not((contains(_isoffsetstring,methodline)) and contains(_ismethodstring,methodline)): #It isn't a method
            return("")
            return(methodline)

def getfieldof(index):
    index = int(index)
    if not(variableexists("dumpcs")):
        objectnotdeclarederror("dumpcs")
        return(None)
    if index > (len(dumpcs)- len("\n")): #Impossible scenario, but ocd makes me put this here!
        return("")
    rangebehind = 0
    startpos = -1
    while startpos == -1:
        startpos = dumpcs.find("\n",((index - rangebehind) - len("\n")),len(dumpcs)) + 1
        if (((index - rangebehind) - len("\n")) < 1): #Not found - must be the beginning (shouldn't happen)
            startpos = 0
            return("") # no field
    endpos = dumpcs.find("\n",startpos + 1,len(dumpcs)) #find the next \n after startpos
    if endpos == -1: #Not found - shouldn't be possible but we assume it is end of dump.cs
        endpos = len(dumpcs) #set to the end
    thisfield = (substring(dumpcs,startpos,endpos)).strip() #field is between new lines
    if not(contains(_isfieldstring,thisfield)): #It isn't a field
            return("")
    return(thisfield)

def getpropertyof(index):
    index = int(index)
    if not(variableexists("dumpcs")):
        objectnotdeclarederror("dumpcs")
        return(None)
    if index > (len(dumpcs)- len("\n")): #Impossible scenario, but ocd makes me put this here!
        return("")
    rangebehind = 0
    startpos = -1
    while startpos == -1:
        startpos = dumpcs.find("\n",((index - rangebehind) - len("\n")),len(dumpcs)) + 1
        if (((index - rangebehind) - len("\n")) < 1): #Not found - must be the beginning (shouldn't happen)
            startpos = 0
            return("") # no field
    endpos = dumpcs.find("\n",startpos + 1,len(dumpcs)) #find the next \n after startpos
    if endpos == -1: #Not found - shouldn't be possible but we assume it is end of dump.cs
        endpos = len(dumpcs) #set to the end
    thisproperty = (substring(dumpcs,startpos,endpos)).strip() #property is between new lines
    if not(contains(_ispropertystring,thisproperty)): #It isn't a property
            return("")
    return(thisproperty)


def getlineof(index,text,removewhitespace = False):
    index = int(index)
    rangebehind = 0
    startpos = -1
    while startpos == -1:
        startpos = text.find("\n",((index - rangebehind) - len("\n")),len(text)) + 1
        if (((index - rangebehind) - len("\n")) < 1): #Not found - must be the beginning
            startpos = 0
            return("") # no field
    endpos = text.find("\n",startpos + 1,len(text)) #find the next \n after startpos
    if endpos == -1: #Not found - must be at the end
        endpos = len(text) #set to the end
    if removewhitespace:
        return((substring(text,startpos,endpos)).strip()) #this line is between new lines
    else:
        return((substring(text,startpos,endpos))) #this line is between new lines

def offsettomethod(offset):
    if offset.startswith("0x"):
        offset = readafter(offset,"0x")
    if not(variableexists("dumpcs")):
        objectnotdeclarederror("dumpcs")
        return(None)
    offsetindex = dumpcs.find(_offsetprefix + offset + _offsetsuffix)
    if offsetindex == -1: #not found
        return("")
    else:
        return(getmethodof(offsetindex))

getmethodofoffset = offsettomethod #same thing, but different name

def offsettofield(classname,offset):
    return("Not Done!")

getfieldofoffset = offsettofield #same thing, but different name

def getobjectofoffset(offset):
    if offset.startswith("0x"):
        offset = readafter(offset,"0x")
    if not(variableexists("dumpcs")):
        objectnotdeclarederror("dumpcs")
        return(None)
    offsetindex = dumpcs.find(_offsetprefix + offset + _offsetsuffix)
    return(getobjectof(offsetindex))

offsettoobject = getobjectofoffset #same thing, but different name


def getnamespaces(objects):
##    namespacenames = []
##    namespacecontent = [] #list of lists (each namespace has list of classes in it)
    namespaces = {}
    i = -1
    for thisobject in objects:
        i = i + 1
        if multipleof(i,1000):
            print(str(i) + "/" + str(len(bjects)))
        thisnamespacename = thisobject["Namespace"]
        if thisnamespacename in namespaces:
            namespaces[thisnamespacename].append(thisobject)
        else:
            namespaces[thisnamespacename] = [thisobject]
    return(namespaces)

def getfullobjects(getshared = True,toremoveattributes = True,toremoveblanklines = True,toremoveallblanklines = False,returntuple = True):
    #Python won't let us declare an object global and set it twice in two different for loops, because it does not know that only one will ever run. So, we have to declare it globa at the start of the function as a workaround.
    global flagremovedblanklines
    fullobjects = dumpcs.split(_objectseparator)
    if len(fullobjects) > 0:
        del fullobjects[0] #classes start with "// Namespace: ", so namespace gets everything before it. This means the first one will always go
    if toremoveblanklines and not(toremoveattributes): #remove blank lines
        new = []
        i = -1
        for thisitem in fullobjects:
            i = i + 1
            if multipleof(i,1000):
                print(str(i) + "/" + str(len(fullobjects)))
            if toremoveallblanklines:
                newitem = removeblanklines(thisitem,True,True,True)
            else:
                newitem = removeblanklines(thisitem)
            new.append(newitem)
        flagremovedblanklines = True
        fullobjects = new
    new = []
    for thisitem in fullobjects: #Add seperator back on, as string.split excludes the seperator
        newitem = _objectseparator + thisitem
        new.append(newitem)
    fullobjects = new
    #fullobjects = tuple(map(lambda x: _objectseparator + x,fullobjects))
    if toremoveattributes: #remove attributes
        new = []
        i = -1
        for item in fullobjects:
            i = i + 1
            if multipleof(i,1000):
                print(str(i) + "/" + str(len(fullobjects)))
            newitem = removeattributes(item,toremoveblanklines)
            new.append(newitem)
        fullobjects = new
        #fullobjects = tuple(map(removeattributes,fullobjects))
        global flagremovedattributes
        flagremovedattributes = True
        if toremoveblanklines:
            flagremovedblanklines = True
    if not(getshared):
        new = []
        i = -1
        for thisitem in fullobjects: #Remove shared objects
            i = i + 1
            if multipleof(i,1000):
                print(str(i) + "/" + str(len(fullobjects)))
            if not(getisshared(thisitem)):
                new.append(thisitem)
        fullobjects = new
        #fullobjects = [thisitem for thisitem in fullobjects if not(getisshared(thisitem))]
        global flagremovedshared
        flagremovedshared = True
    if returntuple:
        return(tuple(fullobjects))
    else:
        return(fullobjects)

def removeattributes(thisobject,toremovenewlines = False):
    global flagremovedattributes
    if flagremovedattributes:
        return(thisobject) #attributes have already been removed!
##    lines = getlines(thisobject,False,False)
##    newlines = []
##    for thisline in lines:
##            newline = removewhitespace(thisline,True,False,False)
##            if ((letter(1,newline) == _attributestart) and (contains(_attributeend,newline))):
##                if contains(_attributeend + " ",newline):
##                    newline = readafter(newline,_attributeend + " ")
##                else:
##                    newline = readafter(newline,_attributeend)
##                if not(newline == ""): #and not((checkforstringat(" " + _isoffsetstring,newline,1)) or (checkforstringat(_isoffsetstring,newline,1)))): # rva is only after we remove compiler generated etc., so it is useless
##                    if((checkforstringat(" " + _isoffsetstring,newline,1)) or (checkforstringat(_isoffsetstring,newline,1))):
##                        newlines.append("\n")
##                newlines.append(newline)
##            else:
##                newline = thisline
##                if not(toremovenewlines and (newline == "")):
##                    if (contains("// RVA: -1 Offset: -1",newline)):
##                        if (len(newlines) == 0):
##                            newlines.append(newline)
##                        else:
##                            if not((checkforstringat(" " + _isoffsetstring,newlines[len(newlines) - 1],1)) or (checkforstringat(_isoffsetstring,newlines[len(newlines) - 1],1))):
##                                newlines.append(newline)
##                            #else:
##                                #newlines[len(newlines) - 1] = newline
##                    else:
##                        if (len(newlines) == 0):
##                            newlines.append(newline)
##                        else:
##                            if not((checkforstringat(" " + _isoffsetstring,newlines[len(newlines) - 1],1)) or (checkforstringat(_isoffsetstring,newlines[len(newlines) - 1],1))):
##                                newlines.append(newline)
##                            else:
##                                newlines[len(newlines) - 1] = newline
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
    return(linestostring(newlines))

def getuserdefinedtype(thisobject):
    thisobject = removeattributes(thisobject)
    global isshared
    isshared = False
    userdefinedtypeofobject = "Other" #in case there are no lines or no words in line 2. not found - unknown structure, so unknown object
    lines = getlines(thisobject,False,False)
    words = getwords(item(_objecttypeline,lines))  #1st line is namespace, 2nd line describes object (abstract class, public enum, etc.)
    onword = 0
    for thisword in words:
        onword = onword + 1
        if onword > len(words): #not found - unknown structure, so unknown object. This should not happen!
            userdefinedtypeofobject = "Other"
            break
        if len(_userdefinedtypes) > 0:
            if thisword in _userdefinedtypes:
                userdefinedtypeofobject = thisword
                #isshared = (contains(".<",(item(2,lines))) or contains(" :",(item(2,lines))) or contains(">.",(item(2,lines)))) #in dump cs, a shared class has '(nameofclass).,' and ' :'.
                isshared = False
                for i in _issharedstrings:
                    if contains(i,item(_objecttypeline,lines)):
                        isshared = True
                        break
                break
    userdefinedtypeofobject = userdefinedtypeofobject.strip()
    return(userdefinedtypeofobject)

getuserdefinedtypeobject = getuserdefinedtype #same thing, but different name
getuserdefinedtypeofobject = getuserdefinedtype #same thing, but different name
objectgetuserdefinedtype = getuserdefinedtype #same thing, but different name

def getisshared(thisobject):
    thisobject = removeattributes(thisobject)
    global isshared
    isshared = False
    lines = getlines(thisobject,False,False)
    words = getwords(item(_objecttypeline,lines))  #1st line is namespace, 2nd line describes object (abstract class, public enum, etc.)
    onword = 0
    for thisword in words:
        onword = onword + 1
        if onword > len(words): #not found - unknown structure, so unknown object. This should not happen!
            isshared = False
            break
        if len(_userdefinedtypes) > 0:
            if thisword in _userdefinedtypes:
                #isshared = (contains(".<",(item(2,lines))) or contains(" :",(item(2,lines))) or contains(">.",(item(2,lines)))) #in dump cs, a shared class has '(nameofclass).,' and ' :'.
                isshared = False
                for i in _issharedstrings:
                    if contains(i,item(_objecttypeline,lines)):
                        isshared = True
                        break #break for optimization - we don't want to go through the whole list if it isn't necessary
            #we check for both of these because they might only have one or the other. there may be false positives, idk. I hope not!
                break
    return(isshared)

getissharedobject = getisshared #same thing, but different name
objectgetisshared = getisshared #same thing, but different name
isshared = getisshared #same thing, but different name
objectisshared = getisshared #same thing, but different name
issharedobject = getisshared #same thing, but different name
getshared = getisshared #same thing, but different name
objectgetshared = getisshared #same thing, but different name
getsharedobject = getisshared #same thing, but different name

def getobjecttype(thisobject):
    thisobject = removeattributes(thisobject)
    typeofobject = ""
    lines = getlines(thisobject,False,False)
    words = getwords(item(_objecttypeline,lines)) #1st line is namespace, 2nd line describes object (abstract class, public enum, etc.)
    onword = 0
    for thisword in words:
        onword = onword + 1
        if onword > len(words): #not found - unknown structure, so unknown object. This should not happen! We assume type is correct anyway.
            break
        if thisword in _userdefinedtypes: #say we want public from public enum, or internal static from internal static class. we... unfinished comment oops
            break
        typeofobject = typeofobject + thisword + " "
    if typeofobject[len(typeofobject) - 1] == "": #we should have gotten a space at the end, since each word, we add the word and " ". We don't want the last space.
        typeofobject = readbefore(typeofobject," ")
    typeofobject = typeofobject.strip()
    return typeofobject

gettypeofobject = getobjecttype #same thing, but different name

def getobjectnamespace(thisobject):
    lines = getlines(thisobject)
    thisline = item(_namespaceline,lines)
    namespacename = readafter(thisline,_namespacenamestart)
    namespacename = namespacename.strip()
    if namespacename == "":
            namespacename = _globalnamespacename
    return(namespacename)

def getobjectname(thisobject):
    thisobject = removeattributes(thisobject)
    lines = getlines(thisobject)
    thisline = item(_objecttypeline,lines) #2nd line is about class, like public static class
    objectname = readbetween(thisline,(getobjecttype(thisobject) + " " + getuserdefinedtype(thisobject) + ""),_objecttypeend)
    if (not(_objectkeepaftercolon) and contains(_objectcolon,objectname)):
        objectname = readbefore(objectname,_objectcolon)
        objectname = substring(objectname,1,len(objectname) - len(_objectcolon)) #readbefore function still keeps up to the end of objectcolon, so remove that
    objectname = objectname.strip()
    return(objectname)

def getmethod(methodname,methodslist,casesensitive = False):
    i = 0
    for thismethod in methodslist:
        i = i + 1
        if match(getmethodname(thismethod),str(methodname),casesensitive):
            thismethod = {
                  "Name" : getmethodname(thismethod),
                  "Type" : getmethodtype(thismethod),
                  "Content" : thismethod,
                  "Offset" : getmethodoffset(thismethod),
                  "Params" : getmethodparams(thismethod),
                  "Param Types" : getmethodparamtypes(thismethod),
                  }
            return(thismethod)
    dumpcsnotfounderror(methodname)
    sys.exit()
    return(None)

def getfield(fieldname,fieldslist,casesensitive = False):
    i = 0
    for thisfield in fieldslist:
        i = i + 1
        if match(getfieldname(thisfield),str(fieldname),casesensitive):
            thisfield = {
                  "Name" : getfieldname(thisfield),
                  "Type" : getfieldtype(thisfield),
                  "Content" : thisfield,
                  "Offset" : getfieldoffset(thisfield),
                  }
            return(thisfield)
    dumpcsnotfounderror(fieldname)
    sys.exit()
    return(None)

def getproperty(propertyname,propertieslist,casesensitive = False):
    i = 0
    for thisproperty in propertieslist:
        i = i + 1
        if match(getpropertyname(thisproperty),str(propertyname),casesensitive):
            thisproperty = {
                  "Name" : getpropertyname(thisproperty),
                  "Type" : getpropertytype(thisproperty),
                  "Content" : thisproperty,
                  "properties" : getpropertyattributes(thisproperty),
                  }
            return(thisproperty)
    dumpcsnotfounderror(propertyname)
    sys.exit()
    return(None)

def getfullmethodparams(thismethod):
    lines = getlines(thismethod)
    thisline = lines[_methodtypeline - 1]
    fullmethodparams = readbetween(thisline,_methodparamsstart,_methodparamsend)
    return(fullmethodparams)

def getmethodparams(thismethod):
    fullmethodparams = getfullmethodparams(thismethod)
    methodparams = []
    thisparam = ""
    ingroup = False
    for thisletter in str(fullmethodparams):
        if ((thisletter == _datatypegroupstart) and not(ingroup)):
           ingroup = True
        if ((thisletter == _datatypegroupend) and ingroup):
           ingroup = False
        if (not(ingroup) and (thisletter == ",")):
            if (thisparam != ""):
                methodparams.append(thisparam.strip())
                thisparam = ""
        else:
            thisparam = (thisparam + thisletter)
    if (thisparam != ""):
                methodparams.append(thisparam.strip())
                thisparam = ""
    return(methodparams)

def getmethodparamtypes(thismethod,replacenames = True):
    #methodparams = getwords(getfullmethodparams(thismethod))
    methodparams = getmethodparams(thismethod)
    newparams = []
    for thisparam in methodparams:
        for thisword in getwords(thisparam):
            newparams.append(thisword)
    methodparams = newparams
    if replacenames:
        methodparams = replacetypenames(methodparams)
    return(methodparams)

def replacetypenames(thistype):
    if _processdatatypegroups:
        #Convert to string
        if type(thistype) == list:
            thistype = wordstostring(thistype)
        #Replace data type groups
        newtypes = ""
        for thisletter in thistype:
                if (thisletter == _datatypegroupstart) or (thisletter == _datatypegroupend) or (thisletter == _datatypegroupseparator) :
                    newtypes = newtypes + " "
                else:
                    newtypes = newtypes  + thisletter
        #Convert to list of words
        words = getwords(newtypes)
    else:
        #Convert to list of words
        if type(thistype) == str:
            words = getwords(thistype)
        else:
            words = thistype
    #Replace names
    newwords = []
    for thisword in words:
        if not(thisword in _types):
            newwords.append(_typenamereplace)
        else:
            newwords.append(thisword)
    if type(thistype) == str:
        newtype = wordstostring(newwords)
    else:
        newtype = newwords
    return(newtype)

def getmethodtype(thismethod,replacenames = True):
    lines = getlines(thismethod)
    thisline = lines[_methodtypeline - 1]
    thisline = substring(thisline,0,findstr(_methodparamsstart,thisline))
    methodtype = readbefore(thisline,_methodparamsstart)
    methodtype = methodtype.strip()
    words = getwords(methodtype)
    if len(words) > 0:
        del words[len(words) - 1]
    methodtype = wordstostring(words)
    if replacenames:
        methodtype = replacetypenames(methodtype)
    return(methodtype)

def getmethodname(thismethod):
    lines = getlines(thismethod)
    thisline = lines[_methodtypeline - 1]
    thisline = substring(thisline,0,findstr(_methodparamsstart,thisline))
    methodname = readbefore(thisline,_methodparamsstart)
    methodname = methodname.strip()
    words = getwords(methodname)
    methodname = words[len(words) - 1]
    return(methodname)

def getmethodoffset(thismethod):
    lines = getlines(thismethod)
    thisline = lines[_methodoffsetline - 1]
    methodoffset = readbetween(thisline,_offsetprefix,_offsetsuffix)
    return(methodoffset)

def removegenericinstmethods(fullmethods):
    lines = getlines(fullmethods,True,True)
    newlines = []
    ingenericinst = False
    for thisline in lines:
        if thisline == _genericinstmethodstart:
            ingenericinst = True
        else:
            if (thisline == _genericinstmethodend) and ingenericinst:
                ingenericinst = False
            else:
                if not(ingenericinst):
                    newlines.append(thisline)
    return(newlines)

def getmethodslist(fullmethods):
    lines = removegenericinstmethods(fullmethods)
    methodslist = []
    if (isodd(len(lines))):
        unexpecteddumpcsformaterror("Methods section missing line or has extra line (only expected sets of 2 lines per method ie:\n         // RVA: 0x1321F3C Offset: 0x1321F3C VA: 0x1321F3C\npublic static float get_deltaTime() { }",fullmethods)
    for i in range(int(len(lines) // 2)):
        methodslist.append(concat([lines[int((((i + 1) * 2)) - 1) - 1],lines[int((((i + 1) * 2))) - 1]],"\n"))
    return(methodslist)

def getmethods(methodslist):
    if type(methodslist) == str: #got full methods, not methods list - so convert to methods list
        methodslist = getmethodslist(methodslist)
    global methods
    methods = []
    for thismethod in methodslist:
        thismethoddata = {
                  "Name" : getmethodname(thismethod),
                  "Type" : getmethodtype(thismethod),
                  "Content" : thismethod,
                  "Offset" : getmethodoffset(thismethod),
                  "Params" : getmethodparams(thismethod),
                  "ParamTypes" : getmethodparamtypes(thismethod),
                  }
        methods.append(thismethoddata)
    return(methods)

def getmethodsdict(methods):
    methodsdict = {}
    for thismethod in methods:
        methodsdict[thismethod["Name"]] = thismethod
    return(methodsdict)


def getfullmethods(thisobject):
    global fullmethods
    thisobject = removeattributes(thisobject)
    lines = getlines(thisobject,True,True)
    if len(lines) > 0:
        if (_methodsstart in lines):
            fullmethods = ""
            i = lines.index(_methodsstart) + 1
            start = i
            thisitem = removewhitespace(lines[i])
            fullmethods = concat([fullmethods,thisitem],"\n")
            i = i + 1
            thisitem = removewhitespace(lines[i])
            i = i + 1
            while not((thisitem in _contentends) or i > (len(lines) - 1)):
                i = i + 1
                if not(iswhitespace(thisitem)):
                    fullmethods = concat([fullmethods,thisitem],"\n")
                thisitem = removewhitespace(lines[i - 1])
        else:
            fullmethods = ""
    return(fullmethods)

def methodsmatch(method1,method2,checkparams = True):
    type1 = method1["Type"]
    type2 = method2["Type"]
    typesmatch = (type1 == type2)
    if checkparams:
        params1 = method1["ParamTypes"]
        params2 = method2["ParamTypes"]
        paramsmatch = (param1 == param2)
    else:
        paramsmatch = True
    return(typesmatch and paramsmatch) #is percentage score not less than tolerated percent?

checkmethods = methodsmatch #same thing, but different name
comparemethods = methodsmatch #same thing, but different name

def getobject(objectnames,fullobjects,casesensitive = False):
    if type(objectnames) == str: #convert to list
        objectnames = [objectnames]
    objectsfound = []
    i = -1
    for thisfullobject in fullobjects:
        i = i + 1
        if multipleof(i,1000):
            print(str(i) + "/" + str(len(fullobjects)))
        if listcontains(getobjectname(thisfullobject),objectnames,casesensitive):
            thisobject = {
                  "Name" : getobjectname(thisfullobject),
                  "Namespace" : getobjectnamespace(thisfullobject),
                  "UserDefinedType" : getuserdefinedtype(thisfullobject),
                  "Shared" : getisshared(thisfullobject),
                  "Type" : getobjecttype(thisfullobject),
                  "Content" : thisfullobject,
                  "Fields" : getfullfields(thisfullobject),
                  "Properties" : getfullproperties(thisfullobject),
                  "Methods" : getfullproperties(thisfullobject),
                  "TypeModel" : buildtypemodel(thisfullobject),
                  }
            objectsfound.append(thisobject)
    if len(objectsfound) < len(objectnames):
        dumpcsnotfounderror(objectname)
        sys.exit()
    return(objectsfound)

def getfieldoffset(thisfield):
    fieldoffset = readafter(thisfield,_fieldoffsetstart)
    return(fieldoffset)

def getfieldtype(thisfield,replacenames = True):
    thisfield = substring(thisfield,0,findstr(_fieldoffsetstart,thisfield))
    fieldtype = readbefore(thisfield,_fieldoffsetstart)
    fieldtype = fieldtype.strip()
    words = getwords(fieldtype)
    if len(words) > 0:
        del words[len(words) - 1]
    fieldtype = wordstostring(words)
    if replacenames:
        fieldtype = replacetypenames(fieldtype)
    return(fieldtype)

def getfieldname(thisfield):
    thisfield = substring(thisfield,0,findstr(_fieldoffsetstart,thisfield))
    fieldname = readbefore(thisfield,_fieldoffsetstart)
    fieldname = fieldname.strip()
    words = getwords(fieldname)
    fieldname = words[len(words) - 1]
    return(fieldname)

def getfieldslist(fullfields):
    lines = getlines(fullfields,True,True)
    global fields
    fields = []
    for thisline in lines:
        if (contains(_fieldoffsetstart,thisline)):
            fields.append(thisline)
    return(fields)

def getfields(fieldslist):
    if type(fieldslist) == str: #got full fields, not fields list - so convert to fields list
        fieldslist = getfieldslist(fieldslist)
    global fields
    fields = []
    for thisfield in fieldslist:
        thisfielddata = {
                  "Name" : getfieldname(thisfield),
                  "Type" : getfieldtype(thisfield),
                  "Content" : thisfield,
                  "Offset" : getfieldoffset(thisfield),
                  }
        fields.append(thisfielddata)
    return(fields)

def getfieldsdict(fields):
    fieldsdict = {}
    for thisfield in fields:
        fieldsdict[thisfield["Name"]] = thisfield
    return(fieldsdict)

def buildtypemodel(thisobject):
    #To do: method params, number of shared classes for class
    objecttype = getobjecttype(thisobject)
    userdefinedtype = getuserdefinedtype(thisobject)
    isshared = getisshared(thisobject)
    fields = getfieldslist(getfullfields(thisobject))
    properties = getpropertieslist(getfullproperties(thisobject))
    methods = getmethodslist(getfullmethods(thisobject))
    fieldtypes = []
    for thisfield in fields:
        fieldtypes.append(getfieldtype(thisfield,True))
    propertytypes = []
    for thisproperty in properties:
        thispropertymodel = {
                            "Type": getpropertytype(thisproperty,True),
                            "Attributes": getpropertyattributes(thisproperty),
                            }
        propertytypes.append(thispropertymodel)
    justpropertytypes = []
    for thisproperty in properties:
        justpropertytypes.append(getpropertytype(thisproperty,True))
    methodtypes = []
    for thismethod in methods:
        thismethodmodel = {
                            "Type": getmethodtype(thismethod,True),
                            "ParamTypes": getmethodparamtypes(thismethod,True),
                            }
        methodtypes.append(thismethodmodel)
    justmethodtypes = []
    for thismethod in methods:
        justmethodtypes.append(getmethodtype(thismethod,True))
    typemodel = {
                  "UserDefinedType": userdefinedtype,
                  "Type": objecttype,
                  "Shared": isshared,
                  "Fields": fieldtypes,
                  "Properties": propertytypes,
                  "PropertyTypes": justpropertytypes,
                  "Methods": methodtypes,
                  "MethodTypes": justmethodtypes,
                  }
    return(typemodel)

gettypemodel = buildtypemodel #same thing, but different name
maketypemodel = buildtypemodel #same thing, but different name

def getfullfields(thisobject):
    global fullfields
    thisobject = removeattributes(thisobject)
    lines = getlines(thisobject,True,True)
    if len(lines) > 0:
        if (_fieldsstart in lines):
            fullfields = ""
            i = lines.index(_fieldsstart) + 1
            start = i
            thisitem = removewhitespace(lines[i])
            fullfields = concat([fullfields,thisitem],"\n")
            i = i + 1
            thisitem = removewhitespace(lines[i])
            i = i + 1
            while not((thisitem in _contentends) or i > (len(lines) - 1)):
                i = i + 1
                if not(iswhitespace(thisitem)):
                    fullfields = concat([fullfields,thisitem],"\n")
                thisitem = removewhitespace(lines[i - 1])
        else:
            fullfields = ""
    return(fullfields)

def getfullproperties(thisobject):
    global fullproperties
    thisobject = removeattributes(thisobject)
    lines = getlines(thisobject,True,True)
    if len(lines) > 0:
        if (_propertiesstart in lines):
            fullproperties = ""
            i = lines.index(_propertiesstart) + 1
            start = i
            thisitem = removewhitespace(lines[i])
            fullproperties = concat([fullproperties,thisitem],"\n")
            i = i + 1
            thisitem = removewhitespace(lines[i])
            i = i + 1
            while not((thisitem in _contentends) or i > (len(lines) - 1)):
                i = i + 1
                if not(iswhitespace(thisitem)):
                    fullproperties = concat([fullproperties,thisitem],"\n")
                thisitem = removewhitespace(lines[i - 1])
        else:
            fullproperties = ""
    return(fullproperties)

def getpropertytype(thisproperty,replacenames = True):
    thisproperty = substring(thisproperty,0,findstr(_propertyattributesstart,thisproperty))
    propertytype = readbefore(thisproperty,_propertyattributesstart)
    propertytype = propertytype.strip()
    words = getwords(propertytype)
    if len(words) > 0:
        del words[len(words) - 1]
    propertytype = wordstostring(words)
    if replacenames:
        propertytype = replacetypenames(propertytype)
    return(propertytype)

def getfullpropertyattributes(thisproperty):
    fullproperties = readbetween(thisproperty,_propertyattributesstart,_propertyattributesend)
    fullproperties = fullproperties.strip()
    words = getwords(fullproperties)
    fullproperties = wordstostring(words)
    return(fullproperties)

def getpropertyattributes(thisproperty):
    fullproperties = getfullpropertyattributes(thisproperty)
    properties = fullproperties.split(_propertyattributeseparator)
    return(properties)

def getpropertyname(thisproperty):
    thisproperty = substring(thisproperty,0,findstr(_propertyattributesstart,thisproperty))
    propertyname = readbefore(thisproperty,_propertyattributesstart)
    propertyname = propertyname.strip()
    words = getwords(propertyname)
    propertyname = words[len(words) - 1]
    return(propertyname)

def getpropertieslist(fullproperties):
    global properties
    lines = getlines(fullproperties,True,True)
    properties = []
    for thisline in lines:
        if (contains(_propertyattributesstart,thisline)):
            properties.append(thisline)
    return(properties)

def getproperties(propertieslist):
    if type(propertieslist) == str: #got full properties, not properties list - so convert to properties list
        propertieslist = getpropertieslist(propertieslist)
    global properties
    properties = []
    for thisproperty in propertieslist:
        thispropertydata = {
                  "Name" : getpropertyname(thisproperty),
                  "Type" : getpropertytype(thisproperty),
                  "Content" : thisproperty,
                  "Attributes" : getpropertyattributes(thisproperty),
		  "FullAttributes" : getfullpropertyattributes(thisproperty),
                  }
        properties.append(thispropertydata)
    return(properties)

def getpropertiesdict(properties):
    propertiesdict = {}
    for thisproperty in properties:
        propertiesdict[thisproperty["Name"]] = thisproperty
    return(propertiesdict)

def getfullclasses(fullobjects):
    fullclasses = []
    i = -1
    for thisobject in fullobjects:
        i = i + 1
        if multipleof(i,1000):
            print(str(i) + "/" + str(len(fullobjects)))
        if getuserdefinedtype(thisobject) == "class":
            fullclasses.append(thisobject)
    return(fullclasses)

def getfullstructs(fullobjects):
    fullstructs = []
    for thisobject in fullobjects:
        if getuserdefinedtype(thisobject) == "struct":
            fullstructs.append(thisobject)
    return(fullstructs)

def getfullenums(fullobjects):
    fullenums = []
    for thisobject in fullobjects:
        if getuserdefinedtype(thisobject) == "enum":
            fullenums.append(thisobject)
    return(fullenums)

def getfullinterfaces(fullobjects):
    fullinterfaces = []
    for thisobject in fullobjects:
        if getuserdefinedtype(thisobject) == "interface":
            fullinterfacse.append(thisobject)
    return(fullinterfaces)

def getobjects(fullobjects,onlyclasses = False,getshared = True,namespacefilter = None,justnameandtypemodel = False,doalphabeticalsort = True,returntuple = True):
    if type(namespacefilter) == str:
        namespacefilter = [namespacefilter] #convert to list
    if namespacefilter == [] or namespacefilter is False:
        namespacefilter = None
    global flagremovedshared
    if onlyclasses:
        fullobjects = getfullclasses(fullobjects)
    objects = []
    i = -1
    for thisfullobject in fullobjects:
        i = i + 1
        if multipleof(i,1000):
            print(str(i) + "/" + str(len(fullobjects)))
        valid = True
        if not(flagremovedshared) and valid:
            if not(getshared):
                if getisshared(thisfullobject):
                    valid = False
        if (namespacefilter != None) and valid:
            if not(getobjectnamespace(thisfullobject) in namespacefilter):
                valid = False
        if valid:
            if justnameandtypemodel:
                thisobject = {
                  "Name" : getobjectname(thisfullobject),
                  "TypeModel" : buildtypemodel(thisfullobject),
                  }
            else:
                objectname = getobjectname(thisfullobject)
                if onlyclasses:
                    userdefinedtype = "class"
                else:
                    userdefinedtype = getuserdefinedtypeofobject(thisfullobject)
                objecttype = getobjecttype(thisfullobject)
                objectnamespace = getobjectnamespace(thisfullobject)
                shared = getisshared(thisfullobject)
                fullmethods = getfullmethods(thisfullobject)
                methods = getmethods(fullmethods)
                methodsdict = getmethodsdict(methods)
                fullfields = getfullfields(thisfullobject)
                fields = getfields(fullfields)
                fieldsdict = getfieldsdict(fields)
                fullproperties = getfullproperties(thisfullobject)
                properties = getproperties(fullproperties)
                propertiesdict = getpropertiesdict(properties)
                typemodel = buildtypemodel(thisfullobject)
                if doalphabeticalsort:
                    methods = alphabeticalsort(methods)
                    fields = alphabeticalsort(fields)
                    properties = alphabeticalsort(properties)
                    methodsdict = alphabeticalsort(methodsdict)
                    fieldsdict = alphabeticalsort(fieldsdict)
                    propertiesdict = alphabeticalsort(propertiesdict)
                thisobject = {
                  "Name" : objectname,
                  "Namespace" : objectnamespace,
                  "UserDefinedType" : userdefinedtype,
                  "Shared" : shared,
                  "Type" : objecttype,
                  "Content" : thisfullobject,
                  "FullMethods" : fullmethods,
                  "Methods" : methods,
                  "MethodsDict" : methodsdict,
                  "FullFields" : fullfields,
                  "Fields" : fields,
                  "FieldsDict" : fieldsdict,
                  "FullProperties" : fullproperties,
                  "Properties" : properties,
                  "PropertiesDict" : propertiesdict,
                  "TypeModel" : typemodel,
                  }
        objects.append(thisobject)
    if doalphabeticalsort:
        objects = alphabeticalsort(objects)
    if not(getshared):
        flagremovedshared = True
    if returntuple:
        return(tuple(objects))
    else:
        return(objects)

findobject = getobject #same thing, but different name

def builddumpcshierarchy(dumpcspath,doalphabeticalsort = True,onlyclasses = False,getshared = True,namespacefilter = None,toremoveattributes = True,toremoveblanklines = True,toremoveallblanklines = False,rettype = "dict"):
    if rettype == dict:
        rettype == "dict"
    elif rettype == list:
        rettype = "list"
    elif rettype == tuple:
        rettype = "tuple"
    elif type(rettype) == str:
        rettype = str(rettype).lower()
    else:
        #Error
        return(None)
    dumpcs = loaddumpcs(dumpcspath)
    if dumpcs is None:
        return(None)
    fullobjects = getfullobjects(getshared,toremoveattributes,toremoveblanklines,toremoveallblanklines,returntuple = True)
    if doalphabeticalsort:
        fullobjects = alphabeticalsort(fullobjects)
    #Sort full objects into list of objects
    objects = getobjects(fullobjects,onlyclasses,getshared,namespacefilter,False,alphabeticalsort,returntuple = True)
    #Sort list of objects into dictionary of namespaces
    namespaces = getnamespaces(objects)
    #Change lists of objects to dictionaries of objects
    newnamespaces = {}
    for thisnamespace, thisobjectlist in zip(namespaces.keys(),namespaces.items()):
        thisobjectdict = {}
        for thisobject in thisobjectlist:
            thisobjectdict[thisobject["Name"]] = thisobject
        newnamespaces[thisnamespace] = thisobjectdict
    if rettype == "dict":
        return(newnamespaces)
    elif rettype == "list":
        return(newnamespaces.items())
    elif rettype == "tuple":
        return(newnamespaces.items())
    else:
        #Unknown ret type - assume dict
        #Warning
        return(newnamespaces)



getdumpcshierarchy = builddumpcshierarchy #same thing, but different name
builddumpcshierarchy = builddumpcshierarchy #same thing, but different name

def typemodelsmatch(model1,model2,usetolerance = None,dosize = True,douserdefinedtype = True,doshared = True,dotype = True,donamespace = True,dofields = True,domethodparams = True,dopropertyattributes = True): #make sure model1 is the unobfuscated one!
    if usetolerance is None:
        global _tolerance
        usetolerance = _tolerance
    #To-do: Number of shared classes for class
    maxscore =(len(model1.get("Methods")) * _methodweighttrue) +  (len(model1.get("Properties")) * _propertyweighttrue) #calculate maximum score
    score = float(0)
    #Size
    if dosize:
        maxscore = maxscore + 8 #start off at 8, and subtract nothing for a perfect score
        size1 = (len(model1.get("Fields")) +  len(model1.get("Methods"))  + len(model1.get("Properties"))) #how many methods, fields, and properties are there?
        size2 = (len(model2.get("Fields")) +  len(model2.get("Methods"))  + len(model2.get("Properties"))) #how many methods, fields, and properties are there?
        score = 8 - (((abs(size2 - size1) / _sizebenchmark) * _sizeweightfalse)) #depending on the difference in size, this could have a small impact, or be very bad
    #Userdefined Type
    if douserdefinedtype:
        maxscore = maxscore + _userdefinedtypeweighttrue
        if model1.get("UserDefinedType") == model2.get("UserDefinedType"):
            score = score + _userdefinedtypeweighttrue
        else:
            return(False) #userdefined type MUST match
    #Shared
    if doshared:
        maxscore = maxscore + _sharedweighttrue
        if model1.get("Shared") == model2.get("Shared"):
            score = score + _sharedweighttrue
        else:
            return(False) #Is shared MUST match
    #Type
##    if dotype:
##        maxscore = maxscore + _objecttypeweighttrue
##        if model1.get("Type") == model2.get("Type"):
##            score = score + _objecttypeweighttrue
    if dotype:
        maxscore = maxscore + _objecttypetrue
        if model1.get("Type") == model2.get("Type"):
            score = score + _objecttypeweighttrue
        else:
            return(False) #Object type MUST match
    #Namespace
    if donamespace:
        maxscore = maxscore + _namespaceweighttrue
        if model1.get("Namespace") == model2.get("Namespace"):
            score = score + _objecttypeweighttrue
    #Fields
    if dofields:
        maxscore = maxscore + (len(model1.get("Fields")) * _fieldweighttrue)
        #We are using the fields type models, not the fields themselvles
        fields1 = list(model1.get("Fields"))
        fields2 = list(model2.get("Fields"))
        templist = list(fields2) #it's very normal to add on things, but not as common to delete them. So, most of the fields in the unobfuscated (earlier) one
        #should also exist in the obfuscated one (newer)
        templist2 = list(fields1)
        for item in templist2:
            if len(templist) > 0:
                if (item in templist):
                    score = score + _fieldweighttrue
                    templist.remove(item)
    #Methods
    if domethodparams:
        #We are using the methods type models, not the methods themselvles
        methods1 = list(model1.get("Methods"))
        methods2 = list(model2.get("Methods"))
    else:
        methods1 = list(model1.get("MethodTypes"))
        methods2 = list(model2.get("MethodTypes"))
    templist = list(methods2) #it's very normal to add on things, but not as common to delete them. So, most of the methods in the unobfuscated (earlier) one
    #should also exist in the obfuscated one (newer)
    templist2 = list(methods1)
    for item in templist2:
            if len(templist) > 0:
                if (item in templist):
                    score = score + _methodweighttrue
                    templist.remove(item)
   #Properties
    if dopropertyattributes:
        #We are using the propertiess type models, not the propertiess themselvles
        properties1 = list(model1.get("Properties"))
        properties2 = list(model2.get("Properties"))
    else:
        properties1 = list(model1.get("PropertyTypes"))
        properties2 = list(model2.get("PropertyTypes"))
    templist = list(properties2) #it's very normal to add on things, but not as common to delete them. So, most of the properties in the unobfuscated (earlier) one
    #should also exist in the obfuscated one (newer)
    templist2 = list(properties1)
    for item in templist2:
            if len(templist) > 0:
                if (item in templist):
                    score = score + _propertyweighttrue
                    templist.remove(item)
    #To do: method params, number of shared classes for class
    matchscore = ((score / maxscore) * 100)
    endspeedtest()
    return(not(((score / maxscore) * 100) < usetolerance)) #is percentage score not less than tolerated percent?

comparetypemodels = typemodelsmatch  #same thing, but different name
checktypemodels = typemodelsmatch #same thing, but different name

def objectscheckformatch(object1,object2,usetolerance = None,dosize = True,douserdefinedtype = True,doshared = True,dotype = True,donamespace = True,dofields = True,domethodparams = True,dopropertyattributes = True):
    #make sure object1 is the unobfuscated one!
    global _trustnames
    if (_trustnames and str(object1.get("Name")) == str(object2.get("Name"))):
        return(True)
    else:
        return(typemodelsmatch(object1.get("TypeModel"),object2.get("TypeModel"),usetolerance,dosize,domethodparams,dopropertyattributes,donamespace))

checkobjects = objectscheckformatch #same thing, but different name
compareobjects = objectscheckformatch #same thing, but different name
objectsmatch = objectscheckformatch #same thing, but different name