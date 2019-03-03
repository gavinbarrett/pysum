#Created by Gavin Barrett on 08-30-18
#!/usr/bin/env python
from hashlib import sha256
import sys
#read in checksum and iso respectively
checksum = sys.argv[1]
isoFile = sys.argv[2]
#get checksum
with open(checksum, 'r') as chksm:
    for line in chksm:
        value = chksm.readline()
        if value.find(isoFile) > -1:
            break
        else:
            if(len(value) == 0):
                value = 0
chksm.close()
value2 = value.split(' *')
value = value2[0]
#blocksize to read file
BLOCKSIZE = 4096
#create hashing obj
hasher = sha256()
with open(isoFile, 'rb') as hashand:
        while True:
            chunk = hashand.read(BLOCKSIZE)
            if not chunk:
                break
            hasher.update(chunk)
hash_string = hasher.hexdigest()
hashand.close()
print('\n')
print("Expected checksum: " + value)
print("Calculated checksum: " + hash_string)
if(value == hash_string):
    print("Good checksum match!")
    print('\n')

