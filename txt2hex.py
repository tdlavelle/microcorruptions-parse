raw_file = open('data/neworleans.txt', "r")
parse_file = open('data/neworleans.bin', "wb")
labels_file = open('data/neworleans.labels', "w")

TOTAL_MEMORY_SIZE = 0xFFFF
last_address = 0x0000

raw_lines = raw_file.readlines()

for line in raw_lines:
    # get rid of extra new lines
    if(not line.strip()): 
        continue
    # get rid of labels
    if(":" not in line[4]):
        labels_file.write(line);
        continue
    # check for continuous address space, add 0s if not
    current_address = int(line[:4], base=16)
    next_address = parse_file.tell()
    if (current_address > next_address):
        # gap found, fill
        for i in range(current_address-next_address):
            parse_file.write(bytes.fromhex("00"))

    # handle program strings
    if('"' in line[:20]):
        string_bytes = bytes(line[6:].replace('"','').replace("\n","\0"), 'utf-8')
        parse_file.write(string_bytes)
        continue
    # extract only the bytes
    hex_strings = line[7:21].split()
    for hex_string in hex_strings:
        hex_bytes = bytes.fromhex(hex_string)
        parse_file.write(hex_bytes)

size = parse_file.tell()-1
#print("size = "+hex(size)+" total = "+hex(TOTAL_MEMORY_SIZE))
# check if padding needed at end
if(size < TOTAL_MEMORY_SIZE):
    for i in range(TOTAL_MEMORY_SIZE-size):
        parse_file.write(bytes.fromhex("00"))

#print("end addr = "+hex(parse_file.tell()))

raw_file.close()
parse_file.close()
