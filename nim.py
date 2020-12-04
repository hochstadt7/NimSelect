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
        sock.connect((hostname, port))
    except OSError as error:
        print("Failed to initialize connection")
        sys.exit(1)

# initialize the connection, game
def nim_client(hostname, port):
    global sock
    create_socket(hostname, port)
    inputs = [sock, sys.stdin]
    outputs = []
    recv_dict = {sys.stdin: "",sock: b""}  # message from server
    send_dict = {sock: b""} # message for server
    expect_input = 0

    while True:
        readable, writable, exp = select(inputs, outputs, [])
        for obj in readable:
            if obj is sys.stdin:
                packed = input()
                recv_dict[obj] += packed
                splitter=recv_dict[obj].split()
                if len(splitter) == 1 and splitter[0] == "Q":  # quit
                    sock.close()
                    sys.exit(1)
                if not expect_input: # input not in client turn get dropped
                    recv_dict[obj] = ""
                else:
                    expect_input = 0
                    if clientfunctions.is_valid_input(recv_dict[obj]):
                        heap_letter, num = recv_dict[obj].split()
                        num = int(num)
                        heap_num = clientfunctions.pick_heap_num(heap_letter)
                        send_dict[sock] = pack(">iii4s", 0, heap_num, num, "mesg".encode())
                    else:
                        send_dict[sock] = pack(">iii4s", 2, 0, 0, "mesg".encode())
                    outputs.append(sock)
                    recv_dict[obj] = ""

            else:
                packed = obj.recv(4)
                if len(packed) == 0: # disconnection
                    print("Disconnected from server")
                    sys.exit(1)
                recv_dict[obj] += packed
                if recv_dict[obj][-4:]== b"mesg":  # message was fully read
                    data=unpack(">iiii",recv_dict[obj][:-4])
                    recv_dict[obj] = b""
                    message_type, heap_A, heap_B, heap_C =data
                    game_continue = clientfunctions.game_seq_progress(message_type, heap_A,heap_B, heap_C)

                    if not game_continue:
                        sock.close()
                        sys.exit(1)
                    if not message_type == 6: # no expected input from client in waiting list
                        expect_input = 1

        for obj in writable:
            bytes_sent = obj.send(send_dict[obj][:4])
            send_dict[obj] = send_dict[obj][bytes_sent:]
            if send_dict[obj] == b"": # message was fully sent
                outputs.remove(obj)



# get inputs for connection of client side

if __name__ == '__main__':
    if len(sys.argv) > 3:
        print("Unappropriate arguments")
        sys.exit(1)

    if len(sys.argv) == 3:
        nim_client(sys.argv[1], int(sys.argv[2]))

    elif len(sys.argv) == 2:
        nim_client(sys.argv[1], 6444)

    else:
        nim_client('localhost', 6444)