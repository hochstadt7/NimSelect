#!/usr/bin/env python3

import socket
import sys
from struct import *
from clientfunctions import game_seq_progress
import client_contact


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
    create_socket(hostname,port)
    while True:
        data= client_contact.my_recv_client(20, sock, [sock, sys.stdin], [], {sock: b"", sys.stdin: b""}, {})
        res=unpack(">iiii",data[:-4])
        message_type,heap_A,heap_B,heap_C=res
        game_continues=game_seq_progress(sock,message_type,heap_A,heap_B,heap_C)
        if game_continues is not True:
            sock.close()
            sys.exit(1)





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

