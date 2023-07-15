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

    def __exit__(self, *args):
        self.socket.close

    def send(self, message):
        self.socket = socket.socket()
        self.socket.connect(self.ip, self.port)
        self.socket.send(message)
        self.socket.close()


from bluetooth import *


class BluetoothServer(object):
    def __init__(self):
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    def __enter__(self):
        self.socket = BluetoothSocket(RFCOMM)
        self.socket.bind(("", PORT_ANY))
        self.socket.listen(1)
        self.port = self.socket.getsockname()[1]

        advertise_service(
            self.socket,
            "MDP-GRP-1",
            service_id=self.uuid,
            service_classes=[self.uuid, SERIAL_PORT_CLASS],
            profiles=[SERIAL_PORT_PROFILE],
            protocols=[OBEX_UUID],
        )

    def __exit__(self, *args):
        self.socket.close()

    def accept(self):
        return self.socket.accept()


if __name__ == "__main__":
    pass
