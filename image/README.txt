# Links
https://medium.com/augmented-startups/train-yolov8-on-custom-data-6d28cd348262

# Commands
pip install ultralytics  

To Train
yolo task=detect mode=train model=yolov8n.pt data=custom.yaml epochs=3 imgsz=640


To Predict
yolo task=detect mode=predict model="runs/detect/train15/weights/best.pt" source="test.png"


# Parameters
model=yolov8s.pt
epochs=10
imgsz=640

augment=False
weight_decay=0.0005