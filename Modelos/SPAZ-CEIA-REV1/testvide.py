from ultralytics import YOLO

# Load a model
model = YOLO("best.pt")  # pretrained YOLO11n model

# Run batched inference on a list of images
#results = model("02-01-03-01-01-01-08.mp4", conf=0.5, max_det=1, iou=0.5)  # return a list of Results objects

results = model("02-01-06-02-01-01-10.mp4") 

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.save(filename="result.jpg")  # save to disk

