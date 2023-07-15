from server import ImageServer
import socket
from ultralytics import YOLO
from PIL import Image

MODEL = YOLO("runs/detect/train23/weights/best.pt")
DIRECTORY = "datasets/data/test/images/"
DIRECTORY = r"/Volumes/pishare/"
if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    ip = '192.168.1.9'
    port = 12345
    print('running ImageServer on ' + ip + ' PORT: ' + str(port))
    
    with ImageServer(ip, port) as s:
        #client, addr = s.accept()
        while True:
            client, addr = s.accept()
            data = client.recv(1024)
            if not data:
                continue
            # get file path from data
            filename = bytes.decode(data, 'utf-8')
            path = DIRECTORY + filename
            print(path)
            # process image
            with Image.open(path) as img:
                result = MODEL.predict(source=img, save=True, show=True, conf=0.6)
                print(result)
                print('---')
                #print(result.len())
                print('---')
                print(result[0].boxes)
                print('---')
                print(result[0].boxes.cls)
                print('---')
                img_id = int((result[0].boxes.cls).numpy())
                print(img_id)
                # return result
                client.sendall(bytes(str(img_id),'utf-8'))
                