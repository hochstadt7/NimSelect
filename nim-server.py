#!/usr/bin/env python3

import socket
import sys
from serverfunctions import *
from struct import *
import server_contact

heaps=[0,0,0]

def create_socket(port):

    global sock
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except OSError as error:
        print("Failed to initialize connection\n")
        sys.exit(1)##do i need to quit like this


# bind the socket to the port
def bind_socket(port):

    global sock
    try:
        sock.bind(('', port))
        sock.listen(1)

    except OSError as error:
        print("Failed to initialize connection\n")
        sys.exit(1)


def nim_server(n_a, n_b, n_c,num_players,wait_list_size ,port):
    global sock
    current_players=[],waiting_list=[]
    create_socket(port)
    bind_socket(port)
    heaps[0] = n_a
    heaps[1] = n_b
    heaps[2] = n_c
    sock.listen(wait_list_size)

    while True:
        # accept
        data= server_contact.my_recv_server()




if __name__ == '__main__':
    if len(sys.argv) != 6 and len(sys.argv) != 7:
        print("Unappropriate arguments\n")
        sys.exit(1)

    if len(sys.argv) == 7:
        nim_server(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
    else:
        nim_server(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), 6444)