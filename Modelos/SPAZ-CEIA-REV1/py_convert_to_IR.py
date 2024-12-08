from ultralytics import YOLO
model = YOLO("best.pt")
model.info()
model.export(format='openvino')
