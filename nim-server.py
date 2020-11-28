#!/usr/bin/env python3

import socket
import sys
from select import select

from serverfunctions import *
from struct import *

def create_socket():

    global sock
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except OSError as error:
        print("Failed to initialize socket\n")
        sys.exit(1)##do i need to quit like this


# bind the socket to the port
def bind_socket(port,wait_list_size):

    global sock
    try:
        sock.bind(('', port))
        sock.listen(wait_list_size)

    except OSError as error:
        print("Failed to initialize binding\n")
        sys.exit(1)


def start_game(sock,num_players,wait_list_size,current_players):
    global heaps
    wait_list=[] # list of waiting players
    wait_and_play=[sock,current_players[0]] # list of waiting players and current players and accepting socket
    recv_dict = {sock: b"",current_players[0]:b""}
    send_dict = {current_players[0]:b""}
    heap_dict={current_players[0]: {"A": heaps["A"],"B": heaps["B"],"C" : heaps["C"]}}
    outputs = current_players
    while current_players:
        readable,writable,exp=select(wait_and_play,outputs,[])
        for obj in readable:
            if obj is sock:
                try:
                    conn, addr = sock.accept()
                    print("connected by: ", addr)
                    if len(current_players)<num_players:
                        wait_and_play.append(conn)
                        current_players.append(conn)
                        send_dict[conn] = pack(">iiii4c", 0, 1, 0, 0,"mesg")  # message to send
                        outputs.append(conn)
                        heap_dict[conn]={"A": heaps["A"],"B": heaps["B"],"C" : heaps["C"]}
                    else:
                        if len(wait_list) < wait_list_size:
                            wait_and_play.append(conn)
                            wait_list.append(conn)
                            send_dict[conn] = pack(">iiii4c", 0, 0, 0, 0, "mesg")  # message to send
                            outputs.append(conn)
                        else:
                             conn.close() # immidiately closeure
                except OSError as error:
                    print("Failed to initialize connection with the client\n")


            else:
                packed = obj.recv(4)  # expect 16 bytes- 3 int's+ 4 chars
                if packed is None:
                    print("Disconnected from client")
                    wait_and_play.remove(obj)
                    if obj in wait_list:
                        wait_list.remove(obj)
                    else:
                        current_players.remove(obj)
                        heap_dict.pop(obj)
                        obj.close()
                    if obj in recv_dict:
                        recv_dict.pop(obj)
                    if obj in send_dict:
                        send_dict.pop(obj)
                    if obj in outputs:
                        outputs.remove(obj)
                    if len(wait_list)>0:
                        # append new player from waiting list
                        new_player=wait_list[0]
                        current_players.append(new_player)
                        recv_dict[new_player]=b""
                        wait_list.remove(new_player)

                else:
                    recv_dict[obj] += packed
                    if recv_dict[obj][-4:] == b"mesg":  # we read all the info
                        outputs.append(obj)
                        data = unpack(">iii", recv_dict[obj][:-4])
                        recv_dict[obj] = b""
                        message_type, heap_num, num_taken = data
                        heaps=bring_heap_letter(heap_num)
                        validity=choice_validity(heap_dict[obj],heap_num,num_taken)
                        cube_left=heap_sum(heaps)
                        if cube_left==0:
                            if validity == "Legal":
                                send_dict[obj]=pack(">iiii4c",3,0,0,0,"mesg")
                            else:
                                send_dict[obj] = pack(">iiii4c", 5, 0, 0, 0, "mesg") # I am not sure this case is possible- illegal move of client and client win? remove this else
                        elif cube_left==1:
                            if validity == "Legal":
                                send_dict[obj] = pack(">iiii4c", 4, 0, 0, 0,"mesg")
                            else:
                                send_dict[obj] = pack(">iiii4c", 5, 1, 0, 0, "mesg") # server win but client move was illegal
                        else:
                            server_heap_choice(heap_dict[obj])
                            send_dict[obj]=pack(">iiii4c",2,heap_dict[obj]["A"],heap_dict[obj]["B"],heap_dict[obj]["C"],"mesg")



        for obj in writable:
            bytes_sent = obj.send(4)  # expect 20 bytes- 3 int's and 4 chars "mesg"
            send_dict[obj] = send_dict[obj + bytes_sent]
            if send_dict[obj] == b"":  # finished to send
                outputs.remove(obj)
                send_dict[obj] =b""


def nim_server(n_a, n_b, n_c,num_players,wait_list_size ,port):
    global sock
    global heaps
    create_socket()
    bind_socket(port,wait_list_size)
    heaps={}
    while True:
        try:
            conn, addr = sock.accept()
            print('Connected by', addr)
        except OSError as error:
            print("Failed accept connection\n")
            sys.exit(1)
        heaps["A"] = n_a
        heaps["B"] = n_b
        heaps["C"] = n_c
        current_players = [conn]

        start_game(sock,num_players,wait_list_size,current_players)




if __name__ == '__main__':
    if len(sys.argv) != 6 and len(sys.argv) != 7:
        print("Unappropriate arguments\n")
        sys.exit(1)

    if len(sys.argv) == 7:
        nim_server(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
    else:
        nim_server(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), 6444)