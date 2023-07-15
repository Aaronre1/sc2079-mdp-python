from ultralytics import YOLO
from PIL import Image

# -- Train Model -- #
# Load model
#model = YOLO("yolov8s.pt")
model = YOLO("runs/detect/train23/weights/best.pt")
#results = model.train(data='custom1.yaml', epochs=20, imgsz=640)

# -- Test Model -- #
#print("Validating...")
#results = model.val()

# from PIL
print("Testing...")
img = Image.open("datasets/data/test/images/test_bullseye.jpg") # input image for detection - from rpi
results = model.predict(source=img, show=True, save=True)  # save plotted images
#print(results)

# -- Retrieve and store detected image label to transfer to rpi for display on android -- #
#detectedLabel = int((results[0].boxes.cls).numpy()) 

#labelFile = open("Detected Label.txt", "w") 
#labelFile.write(str(detectedLabel))
#labelFile.close()