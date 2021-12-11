import sys

TOTAL_MEMORY_SIZE = 0xFFFF

# expect txt file as first (and only) input
if(len(sys.argv) != 2):
    print("USAGE: "+sys.argv[0]+" <text file to parse>")
    exit()

# create file names and files from input
raw_file_name = sys.argv[1]
base_file_name = raw_file_name.rsplit(".", 1)[0]

raw_file = open(raw_file_name, "r")
bin_file = open(base_file_name+".bin", "wb")
labels_file = open(base_file_name+".labels", "w")

# begin parsing
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
    next_address = bin_file.tell()
    if (current_address > next_address):
        # gap found, fill
        for i in range(current_address-next_address):
            bin_file.write(bytes.fromhex("00"))
        # no continue because the line with the gap still needs to be captured below

    # handle program strings
    if('"' in line[:20]):
        string_bytes = bytes(line[6:].replace('"','').replace("\n","\0"), 'utf-8')
        bin_file.write(string_bytes)
        continue
    # extract only the bytes
    hex_strings = line[7:21].split()
    for hex_string in hex_strings:
        hex_bytes = bytes.fromhex(hex_string)
        bin_file.write(hex_bytes)

# check if padding needed at end
size = bin_file.tell()-1
if(size < TOTAL_MEMORY_SIZE):
    for i in range(TOTAL_MEMORY_SIZE-size):
        bin_file.write(bytes.fromhex("00"))

labels_file.close()
raw_file.close()
bin_file.close()
