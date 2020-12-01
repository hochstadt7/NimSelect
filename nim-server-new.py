import socket
import sys
from select import select
from bestmove import *
from serverfunctions import *
from struct import *

HOST = ''  # Standard loopback interface address (localhost)
PORT = 6444        # Port to listen on (non-privileged ports are > 1023)

heaps = {}
num_players = 0
wait_list_size = 0


if len(sys.argv) != 6 and len(sys.argv) != 7:
    print("Inappropriate arguments\n")
    sys.exit(1)

if len(sys.argv) == 7:
    heaps["A"] = int(sys.argv[1])
    heaps["B"] = int(sys.argv[2])
    heaps["C"] = int(sys.argv[3])
    num_players = int(sys.argv[4])
    wait_list_size = int(sys.argv[5])
    PORT = int(sys.argv[6])

else:
    heaps["A"] = int(sys.argv[1])
    heaps["B"] = int(sys.argv[2])
    heaps["C"] = int(sys.argv[3])
    num_players = int(sys.argv[4])
    wait_list_size = int(sys.argv[5])


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", PORT))
sock.listen(wait_list_size)

sockets = [sock]
current_players = []
wait_list = []
outputs = []

recv_dict = {sock: b""}
send_dict = {}
heaps_dict = {}

while True:
    '''In transmission protocol 0:INITIAL MESSAGE, 1:LEGAL, 2:ILLEGAL, 3:WIN, 4:LOSE, 5:ILLEGAL AND GAMEOVER SIMULTANEOUSLY, 6:WAITING LIST' 7:REJECTION'''
    read, write, err = select(sockets, outputs, [])
    for socket in read:
        if socket == sock:
            try:
                conn, addr = sock.accept()
                print("connected by: ", addr)
                if len(current_players) < num_players: # new player

                    sockets.append(conn)
                    current_players.append(conn)
                    outputs.append(conn)

                    heaps_dict[conn] = {"A": heaps["A"], "B": heaps["B"], "C": heaps["C"]}
                    send_dict[conn] = pack(">iiii4s", 0, heaps["A"], heaps["B"], heaps["C"],
                                                   "mesg".encode())
                    recv_dict[conn] = b""

                else:
                    if len(wait_list) < wait_list_size: # wait in the waiting list
                        sockets.append(conn)
                        wait_list.append(conn)
                        outputs.append(conn)

                        send_dict[conn] = pack(">iiii4s", 6, heaps["A"], heaps["B"], heaps["C"],
                                                       "mesg".encode())  # message to send
                        recv_dict[conn] = b""

                    else: # rejection message
                        send_dict[conn] = pack(">iiii4s", 7, heaps["A"], heaps["B"], heaps["C"],
                                               "mesg".encode())
                        sockets.append(conn)
                        outputs.append(conn)


            except OSError as error:
                print("Failed to initialize connection with the client")

        else:
            packed = socket.recv(4)
            if len(packed) == 0: # # disconnection
                print("Disconnected from client")
                refused=0
                sockets.remove(socket)

                if socket in wait_list:
                    wait_list.remove(socket)
                elif socket in current_players:
                    current_players.remove(socket)
                    heaps_dict.pop(socket)
                else: refused=1
                if socket in recv_dict:
                    recv_dict.pop(socket)
                if socket in send_dict:
                    send_dict.pop(socket)
                if socket in outputs:
                    outputs.remove(socket)
                socket.close()

                if len(wait_list) > 0 and not refused: # waiting player is allowed to play

                    new_player = wait_list[0]
                    current_players.append(new_player)
                    outputs.append(new_player)
                    wait_list.remove(new_player)

                    recv_dict[new_player] = b""
                    send_dict[new_player] = pack(">iiii4s", 0, heaps["A"], heaps["B"], heaps["C"],
                                           "mesg".encode())
                    heaps_dict[new_player] = {"A": heaps["A"], "B": heaps["B"], "C": heaps["C"]}


            else:
                recv_dict[socket] += packed
                if recv_dict[socket][-4:] == b"mesg":  # message was fully read
                    outputs.append(socket)
                    data = unpack(">iii", recv_dict[socket][:12])
                    recv_dict[socket] = b""
                    message_type, heap_num, num_taken = data

                    #  illegal input. special case when user input in invalid.
                    if message_type == 2:
                        comp_move(heaps_dict[socket],3)
                        if heap_sum(heaps_dict[socket]) == 0: # illegal input and server win
                            send_dict[socket] = pack(">iiii4s", 5, 0, 0, 0, "mesg".encode())
                        else:
                            send_dict[socket] = pack(">iiii4s", 2, heaps_dict[socket]["A"], heaps_dict[socket]["B"],
                                                 heaps_dict[socket]["C"], "mesg".encode())

                    else:

                        heap_letter = bring_heap_letter(int(heap_num))
                        validity = choice_validity(heaps_dict[socket], heap_letter, num_taken)

                        if validity == 'LEGAL':
                            #  win
                            if heap_sum(heaps_dict[socket]) == 0:
                                send_dict[socket] = pack(">iiii4s", 3, 0, 0,
                                                         0, "mesg".encode())
                            #  regular progression
                            else:
                                comp_move(heaps_dict[socket],3)
                                if heap_sum(heaps_dict[socket]) == 0:
                                    send_dict[socket] = pack(">iiii4s", 4, 0, 0,
                                                             0, "mesg".encode())
                                else:
                                    send_dict[socket] = pack(">iiii4s", 1, heaps_dict[socket]["A"], heaps_dict[socket]["B"],
                                                         heaps_dict[socket]["C"], "mesg".encode())
                        elif validity == 'ILLEGAL':
                            comp_move(heaps_dict[socket], 3)
                            if heap_sum(heaps_dict[socket]) == 0:  # illegal turn and server win
                                send_dict[socket] = pack(">iiii4s", 5, 0, 0, 0, "mesg".encode())
                            else:
                                send_dict[socket] = pack(">iiii4s", 2, heaps_dict[socket]["A"], heaps_dict[socket]["B"],
                                                     heaps_dict[socket]["C"], "mesg".encode())

    for socket in write:
        bytes_sent = socket.send(send_dict[socket][:4])
        send_dict[socket] = send_dict[socket][bytes_sent:]

        if send_dict[socket] == b"":  # message was fully sent
            outputs.remove(socket)