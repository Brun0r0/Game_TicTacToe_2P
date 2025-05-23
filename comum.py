import socket

class Jogador:

    def __init__(self, socket:socket.socket, id = None):
        self.pontos = 0
        self.socket = socket
        self.id = id