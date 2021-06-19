# NimSelect

Web application in server / client structure, for the Nim game.
The server plays in front of several clients. It maintains a waiting list of non-gaming customers, sorted by their login order. The waiting list is completed in turn, which means that as soon as an active player leaves the game, the first player on the waiting list will start playing in front of the server.
The waiting list is limited. Therefore any client can either play in front of the server, be on the waiting list or be rejected by the server.
