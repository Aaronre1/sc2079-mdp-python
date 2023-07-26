from server import ImageServer
import socket
from ultralytics import YOLO
from PIL import Image
import torch

MODEL = YOLO("runs/train/train26/weights/best.pt")
# DIRECTORY = "datasets/data/test/images/"
DIRECTORY = r"/Volumes/pishare/"
IP = "192.168.1.9"

if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    ip = IP
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
                try:
                    result = MODEL.predict(source=img, save=True, show=True, conf=0.5)
                    print(result)
                    labels = torch.tensor(result[0].boxes.cls)
                    label_list = labels.numpy()
                    boxes = result[0].boxes
                    area = 0
                    count = 0
                    largest = 0
                    for box in boxes:
                        b = box.xyxy[0]  # top left bottom right
                        print(b)
                        box_height = b[2] - b[0]
                        box_width = b[3] - b[1]

                        area = int(box_height * box_width)

                        if area > largest:
                            largest = area
                            count += 1

                    print(int(label_list[count - 1]))
                    print("Label list: ", label_list[0])
                    img_id = "15"
                    if len(label_list) != 0:
                        img_id = str(int(label_list[count - 1]))
                        print("Detected image #" + img_id)
                    client.sendall(bytes(img_id, "utf-8"))
                except Exception as e:
                    print(e)
                    client.sendall(b"15")
