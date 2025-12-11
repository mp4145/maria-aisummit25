import cv2
import numpy as np
from backend.detection import detect_objects

# Load any image or first frame of your video
cap = cv2.VideoCapture("data/videos/Crash-1500/000001.mp4")
ret, frame = cap.read()
cap.release()

if ret:
    detections = detect_objects(frame)
    print(f"Found {len(detections)} detections:")
    for x1, y1, x2, y2, conf, cls in detections[:5]:  # First 5
        print(f"  Class {cls}: {conf:.2f} at ({x1},{y1},{x2},{y2})")
else:
    print("Could not read video frame")
