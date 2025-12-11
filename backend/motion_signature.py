# backend/motion_signature.py

import cv2
from typing import Dict, Any, List
from .detection import compute_frame_activity


def compute_motion_signature(video_path: str, event_time_sec: float | None = None) -> Dict[str, Any]:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"timestamps": [], "risk": [], "event_time_sec": event_time_sec}

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    step = max(total_frames // 50, 1)  # ~50 points

    timestamps: List[float] = []
    risk: List[float] = []

    for idx in range(0, total_frames, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, frame = cap.read()
        if not ok:
            break

        t = idx / fps
        activity = compute_frame_activity(frame)  # real model, real output

        timestamps.append(t)
        risk.append(activity)

    cap.release()
    return {
        "timestamps": timestamps,
        "risk": risk,
        "event_time_sec": event_time_sec,
    }
