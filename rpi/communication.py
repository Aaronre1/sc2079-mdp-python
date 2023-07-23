import socket
import requests
import json


class ImageClient(object):
    def __init__(self, ip, port=12345):
        self.ip = ip
        self.port = port

    def send(self, message):
        self.socket = socket.socket()
        self.socket.connect((self.ip, self.port))
        self.socket.send(message)
        result = self.socket.recv(1024)
        self.socket.close()
        return result


class AlgoClient(object):
    def __init__(self, url):
        self.url = url

    def send(self, arena):
        result = requests.post(self.url, json=arena)
        x = json.loads(str(result.text))
        return x


from bluetooth import *


class BluetoothServer(object):
    def __init__(self, uuid):
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

        self.client, self.info = self.socket.accept()

        return self

    def __exit__(self, *args):
        self.socket.close()

    def send(self, message):
        self.client.sendall(message)

    def recv(self, buffer: int = 1024):
        msg = bytes.decode(self.client.recv(buffer), "utf-8")
        return msg

# deprecated
class BluetoothServer2(object):
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
        return self

    def __exit__(self, *args):
        self.socket.close()

    def accept(self):
        return self.socket.accept()

    def send(self, message):
        self.socket.send(message)


def test_algo():
    robot_obstacles_positions = {
        "obstacles": [
            {"x": 5, "y": 5, "d": 0, "id": 3},
            {"x": 12, "y": 5, "d": 0, "id": 7},
        ],
        "robot_x": 1,
        "robot_y": 1,
        "robot_dir": 0,
        "retrying": False,
    }
    url = "http://192.168.1.14:5000/path"
    url = "http://127.0.0.1:5000/path"
    x = requests.post(url, json=robot_obstacles_positions)
    print(x.text)


def test_bluetooth():
    with BluetoothServer() as b:
        client, info = b.accept()
        while True:
            data = client.recv(1024)
            print(str(data))
            if not data:
                break
            client.sendall(data)
        client.close()


if __name__ == "__main__":
    test_algo()
