#Created by Gavin Barrett on 08-30-18
#!/usr/bin/env python3
from hashlib import sha256
from nltk.tokenize import word_tokenize
import sys
import os

def check_arguments():
    ''' Check for argument errors '''
    if  not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
        print('Usage: <checksum.txt> <iso.iso>')
        sys.exit(0)
    if not sys.argv[2].endswith('.iso'):
        print('Usage: <checksum.txt> <iso.iso>')
        sys.exit(0)
    return sys.argv[1], sys.argv[2]

def get_hashsum(hashsum, iso):
    print(hashsum)
    print(iso)
    ''' Receive expected checksum value '''
    with open(hashsum, 'r') as hsum:
        for line in hsum:
            print(line)
            if line.find(iso) != -1:
                # extract hash
                if line.find('SHA256') != -1 or line.find('sha256') != -1 or hashsum.find('SHA256') != -1:
                    tokens = word_tokenize(line)
                    print("Tokens\n")
                    for token in tokens:
                        print(token)
                        if len(token) == 64:
                            return token
        print('Hash retrieval failed..')
        sys.exit(0)

def bar(progress, root,  up):
    ''' update the progress bar '''
    progress['value']+=up
    root.update_idletasks()

def hash_file(isoFile, progress, root):
    ''' Hash the .iso file with sha256 '''
    #blocksize to read file
    BLOCKSIZE = 4096
    #create hashing obj
    hasher = sha256()
    sz = os.path.getsize(isoFile)
    progress.length = sz
    progress.pack()
    with open(isoFile, 'rb') as f:
        print('File length:')
        print(sz)
        while True:
            chunk = f.read(BLOCKSIZE)
            if not chunk:
                break
            hasher.update(chunk)
            bar(progress, root, BLOCKSIZE)
    return hasher.hexdigest()

def authenticated(value, hash_string):
    ''' Authenticate .iso '''
    print('\n')
    print('Expected hash: ' + value)
    print('Calculated hash: ' + hash_string)
    return value == hash_string

def main():
    # check files for basic errors
    hashsum, iso = check_arguments()
    # obtain expected hash value
    value = get_hashsum(hashsum, iso)
    # hash the .iso file
    hash_string = hash_file(iso)
    
    if authenticated(value, hash_string):
        print('Good checksum match!\n')
    else:
        print('Hash values do not match!\n')

if __name__ == "__main__":
    main()
