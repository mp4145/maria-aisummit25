from pathlib import Path
import json
import cv2

BASE_DIR = Path(__file__).resolve().parents[1]
META_PATH = BASE_DIR / "data" / "meta" / "claims.json"

class ClaimNotFound(Exception):
    pass

def load_all_claims():
    with META_PATH.open("r") as f:
        claims = json.load(f)
    return claims

def get_claim_metadata(claim_id: str):
    claims = load_all_claims()
    if claim_id not in claims:
        raise ClaimNotFound(f"Claim {claim_id} not found")
    return claims[claim_id]

def _probe_duration(video_path: Path) -> float:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 10.0  # CCD default if metadata missing
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()

    if frame_count <= 0:
        return 0.0
    return frame_count / fps

def load_claim_with_event_time(claim_id: str):
    """
    Returns:
      {
        ... original metadata ...,
        "abs_video_path": Path,
        "fps": float,
        "duration_sec": float,
        "event_time_sec": float
      }
    """
    meta = get_claim_metadata(claim_id).copy()
    abs_video_path = BASE_DIR / meta["video_path"]
    if not abs_video_path.exists():
        raise FileNotFoundError(f"Video not found: {abs_video_path}")

    # Probe video for fps & duration
    cap = cv2.VideoCapture(str(abs_video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {abs_video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 10.0
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()

    duration_sec = frame_count / fps if frame_count > 0 else 0.0

    event_time_sec = meta.get("event_time_sec")
    if event_time_sec is None:
        # For normal clips, use the middle of the clip
        event_time_sec = duration_sec / 2.0 if duration_sec > 0 else 0.0

    meta.update({
        "abs_video_path": abs_video_path,
        "fps": fps,
        "duration_sec": duration_sec,
        "event_time_sec": event_time_sec
    })
    return meta
