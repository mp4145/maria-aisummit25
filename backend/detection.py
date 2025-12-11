# backend/detection.py

import cv2 
import numpy as np
from pathlib import Path
from typing import Dict, Any

_MODEL_PATH = Path("models/detector/model.onnx")

_net = None

def _get_net():
    global _net
    if _net is None:
        if not _MODEL_PATH.exists():
            raise FileNotFoundError(f"ONNX model not found at: {_MODEL_PATH}")
        _net = cv2.dnn.readNet(str(_MODEL_PATH))

        #_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        #_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    return _net


def compute_frame_activity(frame: np.ndarray) -> float:
    """
    Runs the ONNX model on a frame and returns a scalar 'activity' score
    derived from the raw output tensor. Higher means more complex/active scene.
    """
    net = _get_net()
    blob = cv2.dnn.blobFromImage(
        frame, 1 / 255.0, (640, 640), swapRB=True, crop=False
    )
    net.setInput(blob)
    outs = net.forward()

    # Normalize outs to a list of arrays
    if isinstance(outs, np.ndarray):
        arrays = [outs]
    elif isinstance(outs, (list, tuple)):
        arrays = [a for a in outs if isinstance(a, np.ndarray)]
    else:
        print("Activity score:", score)
        return 0.0

    if not arrays:
        print("Activity score:", score)
        return 0.0

    # Take the largest array and compute an aggregate magnitude
    arr = max(arrays, key=lambda a: a.size)
    # Reduce to scalar: mean absolute activation
    score = float(np.mean(np.abs(arr)))

    # Heuristic normalization: squeeze into [0, 1] range
    # Adjust the divisor if scores are too small/large.
    #score = min(score / 5.0, 1.0)
    score = float(np.mean(np.abs(arr)))
    #score = min(score / 20.0, 1.0)  # larger divisor → less saturation
    score = min(raw * 5.0, 1.0)

    print("Activity score:", score)

    return score
