#Imports labels
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


f = askFile("Select the .labels file for this .bin", "Import labels")

for line in file(f.absolutePath):  # note, cannot use open(), since that is in GhidraScript
  pieces = line.split()
  if (pieces and len(pieces[0]) == 4):
    address = toAddr(long(pieces[0], 16))
    if pieces[1].startswith("<"):
        funcName = pieces[1][1:-1]
        print "creating function", funcName, "at address", address
        createSymbol(address, funcName, False)
        createFunction(address, funcName)
    else:
        print "creating symbol", pieces[1], "at address", address
        createSymbol(address, pieces[1], False)