# object_detector.py
import cv2
import numpy as np

prototxt_path = "/home/unitree/go2_python_sdk/models/MobileNetSSD_deploy.prototxt"
model_path = "/home/unitree/go2_python_sdk/models/MobileNetSSD_deploy.caffemodel"

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

def detect_objects(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found:", image_path)
        return set()

    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)),
                                 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    found = set()
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]
            found.add(label)
    return found
