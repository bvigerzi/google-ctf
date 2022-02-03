# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, secrets, string, time
from flag import flag

## CTF{CR1M3E_0f_d3d_0f_d3dupl1c4ti0n}
## 

def main():
    # It's a tiny server...
    blob = bytearray(2**16)
    files = {}
    used = 0

    # Use d3dupl1c4ti0n to save space.
    def store(data):
        nonlocal used
        MINIMUM_BLOCK = 16
        MAXIMUM_BLOCK = 1024
        part_list = []
        ## what is considered the end of "data"? when the data array is empty :shrug:
        while data:
            prefix = data[:MINIMUM_BLOCK]
            ind = -1
            bestlen, bestind = 0, -1
            while True:
                ## have we already stored this?
                ind = blob.find(prefix, ind+1)
                # if prefix not found in blob
                if ind == -1: break
                # if found, use the length from the longest possible prefix
                #  
                length = len(os.path.commonprefix([data, bytes(blob[ind:ind+MAXIMUM_BLOCK])]))
                # this length would be max 1024, but if data is less than 1024 it would be that length
                # min(1024, len(data)) if they have a commonprefix
                if length > bestlen:
                    bestlen, bestind = length, ind

            ## Yes, then put that in the part list
            if bestind != -1:
                part, data = data[:bestlen], data[bestlen:]
                part_list.append((bestind, bestlen))
            else:
                part, data = data[:MINIMUM_BLOCK], data[MINIMUM_BLOCK:]
                blob[used:used+len(part)] = part
                part_list.append((used, len(part)))
                used += len(part)
                # What happens if this assert fails? Does it crash?
                assert used <= len(blob)

        fid = "".join(secrets.choice(string.ascii_letters+string.digits) for i in range(16))
        ## ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        ##ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ##ascii_letters = ascii_lowercase + ascii_uppercase
        ##digits = '0123456789'
        # fid is an alphanumeric string with 16 characters
        files[fid] = part_list
        return fid

        ## generate a random 16 character string... load... if the result starts with CTF ... then we win ... otherwise keep generating

    def load(fid):
        data = []
        # blob is 64kB of storage
        # it stores blocks, where a block is a minimum of 16 bytes
        # and a max of 1024bytes (1kB)
        # blob -> []
        # flag, flagflag, flagflagflag
        # files:  {'ReluRYhrsZpOHYhV': [(0, 4)], 'dhCjp34Tqpr53lEE': [(4, 8)], '6hhCB4cKxxTBGYUE': [(0, 12)]}
        """
        files:  {'7yrMcZvQFZc0NbwS': [(0, 4)], 'lentPsyEFDVqVKTN': [(4, 8)], '5lrnkG2UwABpP7sq': [(0, 12)]}
        files:  {'7yrMcZvQFZc0NbwS': [(0, 4)], 'lentPsyEFDVqVKTN': [(4, 8)], '5lrnkG2UwABpP7sq': [(0, 12)], 'Zj1XKDqiYKr4vrld': [(0, 12)]}
blob:  bytearray(b'flagflagflag\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x
        """
        for ind, length in files[fid]:
            ## [(0, 4), (5, 12), (2, 2)]
            data.append(blob[ind:ind+length])
            ## it's re-building the string from the cache in the blob
            
        return b"".join(data)

    print("Welcome to our file storage solution.")

    # Store the flag as one of the files.
    # flag = "flag"
    store(bytes(flag, "utf-8"))
    # if flag = "flag"
    # files:  {'wdLjWf6A5TdTmFCR': [(0, 4)]}

    ### connect
    ### CTF{
    ### status --> 0.026kB
    ### YES ?
    ### CTF{a
    ### status --> 0.026kb ?
    ### NO ?
    ### CTF{b
    ### status --> 0.026kb ?
    ### YES !
    ### CTF{ba

    while True:
        print()
        print("Menu:")
        print("- load")
        print("- store")
        print("- status")
        print("- exit")
        choice = input().strip().lower()
        if choice == "load":
            print("Send me the file id...")
            fid = input().strip()
            data = load(fid)
            print(data.decode())
        elif choice == "store":
            print("Send me a line of data...")
            data = input().strip()
            fid = store(bytes(data, "utf-8"))
            print("Stored! Here's your file id:")
            print(fid)
        elif choice == "status":
            print("User: ctfplayer")
            print("Time: %s" % time.asctime())
            kb = used / 1024.0
            kb_all = len(blob) / 1024.0
            print("Quota: %0.3fkB/%0.3fkB" % (kb, kb_all))
            print("Files: %d" % len(files))
        elif choice == "exit":
            break
        else:
            print("Nope.")
            break

try:
    main()
except Exception:
    print("Nope.")
time.sleep(1)
