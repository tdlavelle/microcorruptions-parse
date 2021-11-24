file1 = open('data/neworleans.bin', "rb")
file2 = open('data/neworleans.bin-blah', "rb")

while (byte1 := file1.read(1)):
    if (byte2 := file2.read(1)):
        if (byte1 != byte2):
            print("not equal at: "+hex(file1.tell()))
            quit()
print("probably equal as long as files same length")