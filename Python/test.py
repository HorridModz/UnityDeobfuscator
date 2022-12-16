from DeobfuscationRefactored import *

SPECIALCONSTRUCTORNAMES = True
FIELDPREFIXES = True
with open(dumpcspath, encoding=encoding) as f:
    objects = dumpcs_getobjects(dumpcs_removeattributes(f.read()), getmethodhex=False)
globalnamespace = []
namespaces = {}
for Object in objects:
    hasfields = False
    for field in Object["fields"]:
        if field["hasoffset"]:
            if "__" not in field["name"] and "." not in field["name"] and "<" not in field["name"]:
                hasfields = True
                break
    hasmethods = False
    for method in Object["methods"]:
        if method["hasoffsetdata"]:
            if "__" not in method["name"] and "." not in method["name"] and "<" not in method["name"]:
                hasmethods = True
                break
    if "<" not in Object["name"] and "__" not in Object["name"] and "." not in Object["name"] and (hasfields or hasmethods):
        namespace = Object["namespace"]
        if namespace is None:
            globalnamespace.append(Object)
        else:
            if namespace in namespaces:
                namespaces[namespace].append(Object)
            else:
                namespaces[namespace] = [Object]
code = ""
for Object in globalnamespace:
    hasfields = False
    for field in Object["fields"]:
        if field["hasoffset"]:
            if "__" not in field["name"] and "." not in field["name"] and "<" not in field["name"]:
                hasfields = True
                break
    hasmethods = False
    for method in Object["methods"]:
        if method["hasoffsetdata"]:
            if "__" not in method["name"] and "." not in method["name"] and "<" not in method["name"]:
                hasmethods = True
                break
    if "<" not in Object["name"] and "__" not in Object["name"] and "." not in Object["name"] and (hasfields or hasmethods):
        name = Object["name"]
        code += f"namespace {name}{{"
        usednames = {}
        if hasfields:
            code += "\n\t//Fields"
            for field in Object["fields"]:
                if field["hasoffset"]:
                    if "__" not in field["name"] and "." not in field["name"] and "<" not in field["name"]:
                        if FIELDPREFIXES:
                            if field["name"].startswith("m_"):
                                name = field["name"]
                            elif field["name"].startswith("_"):
                                name = "m" + field["name"]
                            else:
                                name = "m_" + field["name"]
                        else:
                            name = field["name"]
                        if name in usednames:
                            usednames[name] += 1
                            name += str(usednames[name])
                        else:
                            usednames[name] = 1
                        offset = field["offset"]
                        code += f"\n\t\tconst uint64_t {name} = {offset}"
        if hasmethods:
            code += "\n\t//Methods"
            for method in Object["methods"]:
                if method["hasoffsetdata"]:
                    if "__" not in method["name"] and "." not in method["name"] and "<" not in method["name"]:
                        if method["isconstructor"] and SPECIALCONSTRUCTORNAMES:
                            name = "ctor"
                        elif method["isstaticconstructor"] and SPECIALCONSTRUCTORNAMES:
                            name = "cctor"
                        else:
                            name = method["name"]
                        if name in usednames:
                            usednames[name] += 1
                            name += str(usednames[name])
                        else:
                            usednames[name] = 1
                        offset = method["offset"]
                        code += f"\n\t\tconst uint64_t {name} = {offset}"
        code += "\n"
for namespace, objects in namespaces.items():
    code += f"namespace {namespace}{{"
    for Object in objects:
        if "__" not in Object["name"] and "." not in Object["name"] and (hasfields or hasmethods):
            name = Object["name"]
            code += f"\n\tnamespace {name}{{"
            usednames = {}
            if hasfields:
                code += "\n\t\t//Fields"
                for field in Object["fields"]:
                    if field["hasoffset"]:
                        if "__" not in field["name"] and "." not in field["name"] and "<" not in field["name"]:
                            if FIELDPREFIXES:
                                if field["name"].startswith("m_"):
                                    name = field["name"]
                                elif field["name"].startswith("_"):
                                    name = "m" + field["name"]
                                else:
                                    name = "m_" + field["name"]
                            else:
                                name = field["name"]
                            if name in usednames:
                                usednames[name] += 1
                                name += str(usednames[name])
                            else:
                                usednames[name] = 1
                            offset = field["offset"]
                            code += f"\n\t\t\tconst uint64_t {name} = {offset}"
            if hasmethods:
                code += "\n\t\t//Methods"
                for method in Object["methods"]:
                    if method["hasoffsetdata"]:
                        if "__" not in method["name"] and "." not in method["name"] and "<" not in method["name"]:
                            if method["isconstructor"] and SPECIALCONSTRUCTORNAMES:
                                name = "ctor"
                            elif method["isstaticconstructor"] and SPECIALCONSTRUCTORNAMES:
                                name = "cctor"
                            else:
                                name = method["name"]
                            if name in usednames:
                                usednames[name] += 1
                                name += str(usednames[name])
                            else:
                                usednames[name] = 1
                            offset = method["offset"]
                            code += f"\n\t\t\tconst uint64_t {name} = {offset}"
            code += "\n\t}"
    code += "\n}\n\n"
code = code[0:-4] # Lazy way to remove newlines at end
with open(r"C:\Users\zachy\OneDrive\Documents\Work\Temp\Python Temps\offsetstest.cpp", 'w', encoding=encoding) as f:
    f.write(code)
print(code)
