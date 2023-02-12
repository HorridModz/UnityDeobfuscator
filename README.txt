# THIS IS UNFINISHED
**DO NOT TRY TO USE**

A python tool for deobfuscating Unity games.

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