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
    Runs the ONNX model on a frame and returns a scalar 'activity' score.
    Higher means more complex/active scene.
    """
    net = _get_net()
    blob = cv2.dnn.blobFromImage(
        frame, 1 / 255.0, (640, 640), swapRB=True, crop=False
    )
    net.setInput(blob)
    outs = net.forward()

    # Normalize outs to a single ndarray
    if isinstance(outs, np.ndarray):
        arr = outs
    elif isinstance(outs, (list, tuple)):
        arrays = [a for a in outs if isinstance(a, np.ndarray)]
        if not arrays:
            print("Activity score: 0.0 (no arrays)")
            return 0.0
        arr = max(arrays, key=lambda a: a.size)
    else:
        print("Activity score: 0.0 (unexpected outs type)")
        return 0.0

    # Use standard deviation as an activity proxy
    std = float(np.std(arr))
    score = min(std * 10.0, 1.0)  # scale up to make differences visible

    print("Activity score:", score)
    return score
