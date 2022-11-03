A c++ tool for deobfuscating Unity games with lightning speed

Put in apk (il2cpp or mono), dll or dummydll (all or just one), metadata and libil2cpp.so (for il2cpp) or dump.cs (for il2cpp) files of obfuscated and unobfuscated, and it will deobfuscate
Can generate json output, txt output, deobfuscated dll(s), deobfuscated apk, deobfuscated dump.cs, and more!

Features:
-Flexible inputs and outputs
-Automatic Dumping for Il2cpp Games
-Lightning-fast
-Employs 6 deobfuscation methods
-Defeats Beebyte Deobfuscator
-Supports deobfuscation of plugins
-Flexible options
-Force unity version, or it can be auto-detected
-Deobfuscate everything, only one dll / method / class / namespace etc., or specify certain dll > namespace > class > method paths, subpaths (like all classes in blank namespace), regex, name, charset, etc. 
-Dnspy-style viewer for selecting paths etc. 


Options:
-Multi-select deobfuscation methods
-Enable and disable certain things to balance speed and accuracy
-Multi-select plugins to auto-detect and use in deobfuscate
-Multi-select plugins to auto-detect and deobfuscate
-Comes with a few known plugins like Photon and CodeStage, but you can add more by adding apk (il2cpp or mono), dll or dummydll (all or just one), metadata and libil2cpp.so (for il2cpp) or dump.cs (for il2cpp) files and specifying the namespace(s) used by the plugin; the plugin will then be processed and the deobfuscation data will be added to the local database. You can also manually add custom types to trust (such as photoninfo) in methods, fields, and properties
-Specify certain namespaces, classes, or methods to exclude from deobfuscation (in unobfuscated, obfuscated, or both)
-Trust names (if two items have same name, they are a match in deobfuscation)
-Only deobfuscate names with certain naming regex or chars
-Ignore names with certain naming regex or chars when deobfuscating
-Configure output
-Trust Unity types (Vector3, Quaternion, string, etc.)
-Force or auto-detect unity version
-Trust user-defined types
-Trust plugin types
-Configure deobfuscation tolerance
-Choose between only take best match or take all matches
-Change internal settings like size weight and field weight


Deobfuscation Methods:
# - Brute Force Deobfuscation (Comparitive Deobfuscation) : A deobfuscation method that works by comparing unobfuscated and obfuscated dump.cs. It finds the class or member etc. by name. Then, it takes the class, and replaces the names and dynamic values with a certain string ('offset','methodname','classname','comment',etc.). This way, things such as data types, params, # of methods and fields, etc. can be compared. It then converts this into lists of methods, and each method has its method type, and the method params. Same is done on fields and class itself. There is a strikes system with a customizable strictness. It can automatically adapt by narrowing down the perfect strictness by moving it up and down and seeing how little results it can get while still getting results (the toggleable smart mode, changeable in settings or function parameters). This method takes a long time.
# - Regex search deobfuscation (String search deobfuscation): This method is faster, simpler, and better. Both are useful though. This method finds unchanging string (such as <int,float> and private readonly Dictionary<) by searching strings until it finds one with low occurences (like 300 or less), and it finds the one with the lowest. It can also remove names / dynamic values and uses regex search. It can also use the renamer to remove changing things. Then it sees if this comes up in obfuscated. It uses brute force deobfuscation on the resulting classes methods etc. This is done until the right one is found.
# - Mutual Name Deobfuscation (Cross Reference Deobfuscation): This deobfuscation method is kind of like string search deobfuscation. It searches for the name you want to deobfuscate and finds other instances of the name, either as parameters in methods, methods with the same name in other classes, or fields with the same name in other classes. It tries to find one of these where the method or class is unobfuscated, or known through previous deobfuscation. Then, it goes to this class and used brute force deobfuscation to find the right method or field.
# - String Count Deobfuscation: This deobfuscation method is kind of like regex search and mutual name deobfuscation. It compares the number of occurences of a name, string, or regex between game versions.
# - Same Name Deobfuscation: In some games, such as pixel gun 3d, different obfuscated names with the same original names will have the same obfuscated names. This is probably caused by manual find-and-replace-ing. This can be forced by the user, or detected by the program when it finds this out via another form of deobfuscation. When activated, this mode simply finds and replaces text, the same way the names were likely obfuscated - but reversed. This only occurs in weak obfuscation by foolish developers, so don't expect to get lucky with it!
# - Pattern Search Deobfuscation (AOB Deobfuscation): This deobfuscation methods generates aob for an unobfuscated class, method, field, etc., then searches for the aob in the new game version.