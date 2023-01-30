import copy

from DeobfuscationRefactored import *


def compareobjects(object1, object2, dosize = True, dofields = True):
    maxscore = (len(object1["methods"]) * _methodweighttrue) + (
            len(object1["propertiess"]) * _propertyweighttrue)  # calculate maximum score
    score = 0
    # Size
    if dosize:
        maxscore = maxscore + 8  # start off at 8, and subtract nothing for a perfect score
        size1 = (len(object1["fields"]) + len(object1["methods"]) + len(
            object1["propertiess"]))  # how many methods, fields, and properties are there?
        size2 = (len(object2["fields"]) + len(object2["methods"]) + len(
            object2["propertiess"]))  # how many methods, fields, and properties are there?
        score = 8 - (((
                              abs(size2 - size1) / _sizebenchmark) * _sizeweightfalse))  # depending on the difference in size, this could have a small impact, or be very bad
    objectcomparisons: List[Dict[str, bool, Optional[float]]] = [
        {"name": "base", "mustmatch": True, "weight": None},
        {"name": "genericdatatype", "mustmatch": True, "weight": None},
        {"name": "namespace", "mustmatch": True, "weight": None},
        {"name": "hasconstructor", "mustmatch": True, "weight": None},
        {"name": "hasstaticconstructor", "mustmatch": True, "weight": None},
        {"name": "hasfields", "mustmatch": True, "weight": None},
        {"name": "hasproperties", "mustmatch": True, "weight": None},
        {"name": "hasmethods", "mustmatch": True, "weight": None},
    ]
    methodscomparisons: List[Dict[str, bool, Optional[float]]] = [
    ]
    methodweights: List[Dict[str, float]] = [
        {"isconstructor": 7.0},
        {"isstaticconstructor": 7.0},
        {"isoperator": 5.0},
        {"isvirtual": 2.5},
    ] # Anything else is 1
    mustmatch = ["base", "genericdatatype", "namespace", "hasconstructor",
                 "hasstaticconstructor", "hasfields", "hasproperties", "hasmethods"]
    for must in mustmatch:
        if not (object1[must] == object2[must]):
            return 0
    # Fields
    if dofields:
        maxscore = maxscore + (len(object1["fields"]) * _fieldweighttrue)
        # We are using the fields type objects, not the fields themselvles
        fields1 = copy.deepcopy(object1["fields"])
        fields2 = list(object2["fields"])
        templist = list(
            fields2)  # it's very normal to add on things, but not as common to delete them. So, most of the fields in the unobfuscated (earlier) one
        # should also exist in the obfuscated one (newer)
        templist2 = list(fields1)
        for item in templist2:
            if len(templist) > 0:
                if (item in templist):
                    score = score + _fieldweighttrue
                    templist.remove(item)
    # Methods
    if domethodparams:
        # We are using the methods type objects, not the methods themselvles
        methods1 = list(object1["methods"])
        methods2 = list(object2["methods"])
    else:
        methods1 = list(object1.get("MethodTypes"))
        methods2 = list(object2.get("MethodTypes"))
    templist = list(
        methods2)  # it's very normal to add on things, but not as common to delete them. So, most of the methods in the unobfuscated (earlier) one
    # should also exist in the obfuscated one (newer)
    templist2 = list(methods1)
    for item in templist2:
        if len(templist) > 0:
            if (item in templist):
                score = score + _methodweighttrue
                templist.remove(item)
    # Properties
    if dopropertyattributes:
        # We are using the propertiess type objects, not the propertiess themselvles
        properties1 = list(object1["propertiess"])
        properties2 = list(object2["propertiess"])
    templist = list(
        properties2)  # it's very normal to add on things, but not as common to delete them. So, most of the properties in the unobfuscated (earlier) one
    # should also exist in the obfuscated one (newer)
    templist2 = list(properties1)
    for item in templist2:
        if len(templist) > 0:
            if (item in templist):
                score = score + _propertyweighttrue
                templist.remove(item)
    # To do: method params, number of shared classes for class
    matchscore = ((score / maxscore) * 100)
    endspeedtest()
    return (not (((score / maxscore) * 100) < usetolerance))  # is percentage score not less than tolerated percent?
