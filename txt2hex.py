raw_file = open('data/neworleans.txt', "r")
parse_file = open('data/neworleans.bin', "wb")

raw_lines = raw_file.readlines();

for i in range(0x4400):
    parse_file.write(bytes.fromhex("00"))

for line in raw_lines:
    # get rid of extra new lines
    if(not line.strip()): 
        continue
    # get rid of labels
    if(":" not in line[4]):
        continue
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
