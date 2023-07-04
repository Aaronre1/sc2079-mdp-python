from ultralytics import YOLO
from PIL import Image
import cv2

# -- Train Model -- #
# Load model
#model = YOLO("yolov8s.pt")
model = YOLO("runs/detect/train/weights/best.pt")
#results = model.train(data='custom.yaml', epochs=10, imgsz=640)

# -- Test Model -- #
#results = model.val()

# from PIL
img = Image.open("datasets/data/test/images/multi_64.jpeg")
results = model.predict(source=img, save=True)  # save plotted images
print(results)
detectedImg = Image.open('runs/detect/predict/multi_64.jpeg')
detectedImg.show()
