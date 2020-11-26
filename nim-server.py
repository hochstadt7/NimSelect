#!/usr/bin/env python3

import socket
import sys
from select import select

from serverfunctions import *
from struct import *

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


def start_game(sock,heaps,num_players,wait_list_size,current_players):
    wait_list=[] # list of waiting players
    wait_and_play=[sock,current_players[0]] # list of waiting players and current players and accepting socket
    recv_dict = {sock: b"",current_players[0]:b""}
    send_dict = {current_players[0]:b""}
    while current_players:
        readable,writable,exp=select(wait_and_play,current_players,[])
        for obj in readable:
            if obj is sock:
                conn, addr = sock.accept()
                print("connected by: ", addr)
                if len(current_players)<num_players:
                    wait_and_play.append(conn)
                    current_players.append(conn)
                    send_dict[conn] = pack(">iiii4c", 0, 1, 0, 0,"mesg")  # message to send
                else:
                    if len(wait_list) < wait_list_size:
                        wait_and_play.append(conn)
                        wait_list.append(conn)
                        send_dict[conn] = pack(">iiii4c", 0, 0, 0, 0, "mesg")  # message to send
                    # need to make else case if get refused connection?
            else:
                packed = obj.recv(4)  # expect 12 bytes- 3 int's
                if packed is None:
                    print("Disconnected from client")
                    wait_and_play.remove(obj)
                    if obj in wait_list:
                        wait_list.remove(obj)
                    else:
                        current_players.remove(obj)
                    if obj in recv_dict:
                        recv_dict.pop(obj)
                    if obj in send_dict:
                        send_dict.pop(obj)
                    if len(wait_list)>0:
                        # append new player from waiting list
                        new_player=wait_list[0]
                        current_players.append(new_player)
                        recv_dict[new_player]=b""
                        wait_list.remove(new_player)

                else:
                    recv_dict[obj] += packed
                    if recv_dict[obj][-4:] == b"mesg":  # we read all the info
                        data = unpack(">iii", recv_dict[obj][:-4])
                        message_type, heap_num, num_taken = data
                        heaps=bring_heap_letter(heap_num)
                        validity=choice_validity(heaps)
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
                            server_heap_choice(heaps)
                            send_dict[obj]=pack(">iiii4c",2,heaps[0],heaps[1],heaps[2],"mesg")


        for obj in writable:
            bytes_sent = obj.send(4)  # expect 20 bytes- 3 int's and 4 chars "mesg"
            send_dict[sock] = send_dict[sock + bytes_sent]
            if send_dict[sock] == b"":  # finished to send
                send_dict[obj] = b""



def nim_server(n_a, n_b, n_c,num_players,wait_list_size ,port):
    global sock
    create_socket(port)
    bind_socket(port)
    sock.listen(wait_list_size)

    while True:
        try:
            conn, addr = sock.accept()
            print('Connected by', addr)
        except OSError as error:
            print("Failed accept connection\n")
            sys.exit(1)
        heaps[0] = n_a
        heaps[1] = n_b
        heaps[2] = n_c
        current_players = [conn]

        start_game(heaps,num_players,wait_list_size,current_players)




if __name__ == '__main__':
    if len(sys.argv) != 6 and len(sys.argv) != 7:
        print("Unappropriate arguments\n")
        sys.exit(1)

    if len(sys.argv) == 7:
        nim_server(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
    else:
        nim_server(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), 6444)