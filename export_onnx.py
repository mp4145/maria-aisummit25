from ultralytics import YOLO

# 1) Pick a model:
#    - If you have your own trained .pt, put its path here
#    - Otherwise use a small pre-trained model for the demo:
# model = YOLO("path/to/your_model.pt")
model = YOLO("yolov8n.pt")  # small, good for demo

model.export(
    format="onnx",
    opset=12,      # good compatibility with OpenCV
    dynamic=False, # fixed input size, simpler
    imgsz=640,     # match what you want for inference
    simplify=True,
)
print("Exported to ONNX")
