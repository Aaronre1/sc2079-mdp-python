import socket


class ImageServer(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __enter__(self):
        self.socket = socket.socket()
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        return self

    def __exit__(self, *args):
        self.socket.close()

    def accept(self):
        return self.socket.accept()


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 12345
    with ImageServer(ip, port) as s:
        client, addr = s.accept()
        while True:
            data = client.recv(1024)
            print(str(data))
            if not data:
                break
            client.sendall(data)
