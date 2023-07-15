from server import ImageServer
import socket
from ultralytics import YOLO
from PIL import Image

MODEL = YOLO("runs/detect/train/weights/best.pt")
DIRECTORY = "datasets/data/test/images/"
DIRECTORY = r"//192.168.1.1/pishare/"
DIRECTORY = r"~/Volumes/pishare/"
DIRECTORY = r"/Volumes/pishare/"
if __name__ == "__main__":
    print('test')
    ip = socket.gethostbyname(socket.gethostname())
    ip = '192.168.1.9'
    print(ip)
    port = 12345
    with ImageServer(ip, port) as s:
        client, addr = s.accept()
        while True:
            data = client.recv(1024)

            # get file path from data
            filename = bytes.decode(data, 'utf-8')
            path = DIRECTORY + filename
            print(path)
            # process image
            with Image.open(path) as img:
                result = MODEL.predict(source=img, save=True)
                print(result)
                # return result
                client.sendall(b'1')
                