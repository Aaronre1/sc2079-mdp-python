from ultralytics import YOLO
from PIL import Image
import cv2
#filename = 'bullseye.jpg'
#filename = 'circle.jpg'
#filename = 'eight.jpg'
#filename = 'nine.jpg'
#filename = 'cc.jpg'
filename = 'something.jpg'
# -- Train Model -- #
# Load model
#model = YOLO("yolov8s.pt")
model = YOLO("runs/detect/train/weights/best.pt")
#results = model.train(data='custom.yaml', epochs=10, imgsz=640)

# -- Test Model -- #
#results = model.val()

# from PIL
img = Image.open("datasets/data/test/images/"+filename)
results = model.predict(source=img, save=True)  # save plotted images
print(results)
detectedImg = Image.open('runs/detect/predict/'+filename)
detectedImg.show()
