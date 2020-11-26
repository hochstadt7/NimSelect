#!/usr/bin/env python3

import socket
import sys
from struct import *
import clientfunctions
from select import select


def create_socket(hostname, port):
    global sock

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as error:
        print("Failed to initialize connection\n")
        sys.exit(1)
    try:
        sock.connect((hostname, port))
    except OSError as error:
        print("You are rejected by the server.\n")
        sys.exit(1)

# initialize the connection, game
def nim_client(hostname, port):
    global sock
    inputs=[sys.stdin]
    outputs = []
    recv_dict={sys.stdin:"",sock:b""} # is it important to append sock to list after create_socket()? don't think so..
    send_dict = {sock:b""}
    expect_input=0
    create_socket(hostname,port)
    while True:
        readable,writable,exp=select(inputs,outputs,[])
        for obj in readable:
            if obj is sys.stdin:
                packed = obj.recv(3)
                recv_dict[obj] += packed
                if recv_dict[obj][-1:] == "\n":
                    if len(recv_dict[obj])==1 and recv_dict[obj] == "Q": # quit
                        sock.close()
                        sys.exit(1)
                    if not expect_input:
                        recv_dict[obj]="" # too early input get dropped?
                    else:
                        expect_input=0 # cuz now we already have input
                        if clientfunctions.is_valid_input(recv_dict[obj]):
                            heap_letter, num = recv_dict[obj].split()
                            num = int(num)
                            heap_num = clientfunctions.pick_heap_num(heap_letter)
                            send_dict[sock]=pack(">iii4c", 0, heap_num, num,"mesg") # message for server
                        else:
                            send_dict[sock]=pack(">iii4c", 2, 0, 0,"mesg")
                        outputs.append(sock)  # want to be able to send to server
                        recv_dict[sys.stdin]=""

            else:
                packed = obj.recv(4) # expect 20 bytes- 3 int's and 4 chars "mesg"
                if packed is None:
                    print("Disconnected from server\n")
                    sys.exit(1)
                recv_dict[obj] += packed
                if recv_dict[obj][-4:] == b"mesg":  # we read all the info
                    data=unpack(">iiii",recv_dict[obj][:-4])
                    message_type, heap_A, heap_B, heap_C =data
                    expect_input=1
                    game_continue= clientfunctions.game_seq_progress(message_type, heap_A)
                    if not game_continue:
                        sock.close()
                        sys.exit(1)

        for obj in writable:
            bytes_sent=obj.send(4) # expect 12 bytes- 3 int's
            send_dict[sock] =send_dict[sock+bytes_sent]
            if send_dict[sock]==b"": # finished to send
                outputs.remove(obj)
                send_dict[obj]=b""


# get inputs for connection of client side
if __name__ == '__main__':
    if len(sys.argv) > 3:
        print("Unappropriate arguments\n")
        sys.exit(1)

    if len(sys.argv) == 3:
        nim_client(sys.argv[1], int(sys.argv[2]))

    elif len(sys.argv) == 2:
        nim_client(sys.argv[1], 6444)

    else:
        nim_client('localhost', 6444)

