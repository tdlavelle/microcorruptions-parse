raw_file = open('data/neworleans.txt', "r")
parse_file = open('data/neworleans.bin-blah', "wb")
TOTAL_MEMORY_SIZE = 0xFFFF
last_address = 0x0000

raw_lines = raw_file.readlines()

#for i in range(0x4400):
    #parse_file.write(bytes.fromhex("00"))

for line in raw_lines:
    # get rid of extra new lines
    if(not line.strip()): 
        continue
    # get rid of labels
    if(":" not in line[4]):
        continue
    # check for continuous address space, add 0s if not
    current_address = int(line[:4], base=16)
    if(last_address == 0 and current_address == 0):
        # raw file starts at 0x0000, process normal
        last_address = current_address
    elif(current_address > last_address+6):
        # jump occurred in address space, fill with 0s
        for i in range(current_address-last_address):
            parse_file.write(bytes.fromhex("00"))
        last_address = current_address
    elif(current_address >= last_address+2):
        # normal processing of contiguous memory, instructions can be 2 or 4 bytes
        last_address = current_address
    else:
        print("ERROR: current_address ["+hex(current_address)+"] < last_address+2 ["+hex(last_address)+2+"]")
    # handle program strings
    if('"' in line[:20]):
        parse_file.write(bytes(line[6:].replace('"','').replace("\n","\0"), 'utf-8'))
        continue
    # extract only the bytes
    hex_strings = line[7:21].split()
    for hex_string in hex_strings:
        hex_bytes = bytes.fromhex(hex_string)
        #print(hex_string+"\t"+hex_bytes.hex())
        parse_file.write(hex_bytes)

raw_file.close()
parse_file.close()
