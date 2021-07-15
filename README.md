# NimSelect

Web application in a server / client structure, for the Nim game.
The server plays against several clients. It maintains a waiting list of non-gaming customers, sorted by their login order. The waiting list is completed in turn, which means that as soon as an active player leaves the game, the first player on the waiting list will start playing against the server.
The waiting list is limited, therefore any client can either play against the server, be on the waiting list or be rejected by the server.
