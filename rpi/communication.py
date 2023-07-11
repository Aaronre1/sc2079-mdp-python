import socket

SOCK = socket.socket()
PORT = 12345
IP = "192.168.1.9"


def send(message):
    SOCK.connect(IP, PORT)
    SOCK.send(message)
    SOCK.close()
    