from server import ImageServer
import socket
from ultralytics import YOLO
from PIL import Image
import torch

MODEL = YOLO("runs/detect/train23/weights/best.pt")
DIRECTORY = "datasets/data/test/images/"
DIRECTORY = r"/Volumes/pishare/"
# TODO: Setup DIRECTORY for Windows
if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    ip = "192.168.1.16"
    port = 12345
    print("running ImageServer on " + ip + " PORT: " + str(port))

    with ImageServer(ip, port) as s:
        while True:
            client, addr = s.accept()
            data = client.recv(1024)
            if not data:
                continue
            # get file path from data
            filename = bytes.decode(data, "utf-8")
            path = DIRECTORY + filename
            print(path)
            # process image
            with Image.open(path) as img:
                # try:
                    result = MODEL.predict(source=img, save=True, show=True, conf=0.5)
                    print(result)
                    labels = torch.tensor(result[0].boxes.cls)
                    label_list = labels.numpy()
                    print("Label list: ", label_list[0])
                    img_id = "15"
                    if len(label_list) != 0:
                        img_id = str(int(label_list[0]))
                        print("Detected image #" + img_id)
                    client.sendall(bytes(img_id, "utf-8"))
                # except:
                #     print("exception")
                #     client.sendall(b"15")
