import socket

# SOCK = socket.socket()
# PORT = 12345
# IP = "192.168.1.9"


# def send(message):
#     SOCK.connect(IP, PORT)
#     SOCK.send(message)
#     SOCK.close()


# def open_socket(ip):
#     address = (ip, PORT)
#     conn = socket.socket()
#     conn.bind(address)
#     conn.listen(1)
#     print(conn)
#     return conn


# ip = "192.168.1.1"
# conn = open_socket(ip)
# while True:
#     client = conn.accept()[0]
#     data = client.recv(1024)
#     print(data)
#     client.sendall(b"PONG")
#     client.close()
#     if not data:
#         break
# conn.close()


class ImageClient(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __enter__(self):
        self.socket = socket.socket()
        self.socket.connect(self.ip, self.port)
        
    def __exit__(self,*args):
        self.socket.close
        
    def send(self, message):
        self.socket = socket.socket()
        self.socket.connect(self.ip, self.port)
        self.socket.send(message)
        self.socket.close()
