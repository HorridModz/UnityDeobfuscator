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
    checks = ("// Image 0:","// Namespace:","class","	// Methods","// RVA: 0x")
    for check in checks:
        if not check in dumpcs:
            return(False)
    return(True)

with open(r"C:\Users\zachy\OneDrive\Documents\Work\Projects\Pixel Gun 3D\Pixel Gun 3D 16.6.1\servertemp.txt",encoding='utf8') as f:
    print(dumpcs_isvalid(f.read()))