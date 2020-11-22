#!/usr/bin/env python3

import socket
import sys
import struct
from select import select
from struct import *
from clientfunctions import game_seq_progress


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
    there_is_input=0 # input accepted?
    create_socket(hostname,port)
    inputs=[sys.stdin,sock], outputs=[sock]
    soc_to_mess={sys.stdin:b"",sock:b""}
    while True:
        readable,writeable,exp=select(inputs,outputs,[])
        for obj in readable:
            if obj is sock:
                packed = obj.recv(20)  # 4*4+4 in case of sock
                if packed is None:
                    print("Disconnected from server\n")
                    sys.exit(1)
                data = unpack(">iiii", packed)
                soc_to_mess[obj] += data
                if soc_to_mess[obj][-4:]==b"mesg":
                    message_type, heap_A, heap_B, heap_C = soc_to_mess[obj][:4]
                    if there_is_input:
                        game_continues = game_seq_progress(obj, message_type, heap_A, heap_B, heap_C)
            '''else:
                msg=obj.recv(12)
                if len(msg)==0: # need to change condition
                    there_is_input=1
                else:
                    soc_to_mess[obj] +=msg'''


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

