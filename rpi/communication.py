import socket


class ImageClient(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send(self, message):
        self.socket = socket.socket()
        self.socket.connect((self.ip, self.port))
        self.socket.send(message)
        result = self.socket.recv(1024)
        self.socket.close()
        return result


from bluetooth import *


class BluetoothServer(object):
    def __init__(self, uuid="94f39d29-7d6d-437d-973b-fba39e49d4ee"):
        self.uuid = uuid

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
    with BluetoothServer() as b:
        client, info = b.accept()
        while True:
            data = client.recv(1024)
            print(str(data))
            if not data:
                break
            client.sendall(data)
        client.close()
