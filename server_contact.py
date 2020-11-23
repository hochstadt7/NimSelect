from select import select
import socket
import sys
import struct
from struct import *


def my_recv_server(num_bytes,main_sock,connection,inputs,outputs,recv_dict,send_dict):

    # need to add a counter to the length of the waiting clients to change it dinamicly

    while True:
        readable,writeable,exp=select(inputs,outputs,[])

        for obj in readable:
            if obj is connection:
                new_conn,addr=obj.accept()
                # need to check waiting list
                inputs.add(obj)
                outputs.add(obj)
                recv_dict[new_conn]=b""
                send_dict[new_conn] = b""

            elif obj is main_sock:
                packed=obj.recv(num_bytes)
                if packed is None:
                    print("Disconnected from client\n")
                    inputs.remove(obj)
                    outputs.remove(obj)
                    recv_dict.pop(obj)
                    send_dict.pop(obj)
                    obj.close()
                else:
                    recv_dict[obj] += packed
                    if recv_dict[obj][-4:] == b"mesg": # we read all info for main_sock
                        return

            else:
                packed = obj.recv(num_bytes)
                if packed is None:
                    print("Disconnected from client\n")
                    inputs.remove(obj)
                    outputs.remove(obj)
                    recv_dict.pop(obj)
                    send_dict.pop(obj)
                    obj.close()
                else:
                    recv_dict[obj] += packed
                    if recv_dict[obj][-4:] == b"mesg":
                        if recv_dict[obj]=="Q":
                            inputs.remove(obj)
                            outputs.remove(obj)
                            recv_dict.pop(obj)
                            send_dict.pop(obj)
                        recv_dict[obj]=b""

        for obj in writeable:
            if send_dict[obj]!="":
                bytes_sent=obj.send(send_dict[obj])
                send_dict[obj]=send_dict[obj+bytes_sent]

def my_send_server(num_bytes,main_sock,inputs,outputs,recv_dict,send_dict):
