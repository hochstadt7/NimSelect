from select import select
import socket
import sys
import struct
from struct import *


def my_recv_client(num_bytes,main_sock,inputs,outputs,recv_dict,send_dict):
    while True:
        readable,writeable,exp=select(inputs,outputs,[])
        for obj in readable:
            if obj is main_sock:
                packed=obj.recv(num_bytes)
                if packed is None:
                    print("Disconnected from server\n")
                    sys.exit(1)
                recv_dict[obj] += packed
                if recv_dict[obj][-4:] == b"mesg": # we read all info for main_sock
                    return
            else:
                packed=obj.recv(12)
                recv_dict[obj] += packed
                if recv_dict[obj][-1:]=="\n":
                    if recv_dict[obj]=="Q":
                        main_sock.close()
                        sys.exit(1)
                    recv_dict[obj]="" # too early input

        for obj in writeable:
            if send_dict[obj] != "":
                bytes_sent=obj.send(send_dict[obj])
                send_dict[obj]=send_dict[obj+bytes_sent]

def my_send_client(num_bytes,main_sock,inputs,outputs,recv_dict,send_dict):
    while True:
        readable,writeable,exp=select(inputs,outputs,[])
        for obj in readable:
            if obj is sys.stdin:
                packed = obj.recv(12)
                recv_dict[obj] += packed
                if recv_dict[obj][-1:] == "\n":
                    if recv_dict[obj] == "Q":
                        main_sock.close()
                        sys.exit(1)
                    recv_dict[obj] = ""  # too early input

        for obj in writeable:
            if obj is main_sock:
                if send_dict[obj] != "":
                    bytes_sent = obj.send(send_dict[obj])
                    send_dict[obj] = send_dict[obj + bytes_sent]
                else:
                    return

