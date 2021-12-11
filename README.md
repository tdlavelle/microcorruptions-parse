# microcorruptions-parse
Parses of microcorruptions.com for Ghidra import

From Microcorruptions.com, copy the contents of the entire disassembly window and save to a text file.

Run txt2hex.py on it to generate a .bin and .labels file.
The .bin can be imported into ghidra to analyze. The .labels file will be used by the mc-import-labels.py ghidra script to add labels to the disassembled .bin file.

Import mc-import-labels.py to Ghidra, either copy to an existing Ghidra script directory or add repo as a script directory to be able to load it.
