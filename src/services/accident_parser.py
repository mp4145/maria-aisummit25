from typing import Dict
from ..core.schemas import AccidentAnalysisRequest


def normalize_seat_position(raw: str) -> str:
    raw = raw.lower().strip()
    mapping = {
        "driver": "driver",
        "front": "front_passenger",
        "front_passenger": "front_passenger",
        "rear_left": "rear_left",
        "rear_right": "rear_right",
        "rear_center": "rear_center",
        "back_left": "rear_left",
        "back_right": "rear_right",
        "back_middle": "rear_center",
    }
    return mapping.get(raw, raw)


def normalize_impact_side(raw: str) -> str:
    raw = raw.lower().strip()
    if "rear" in raw or "back" in raw:
        return "rear"
    if "front" in raw:
        return "front"
    if "left" in raw:
        return "left"
    if "right" in raw:
        return "right"
    if "roll" in raw:
        return "rollover"
    if "multi" in raw:
        return "multi"
    return raw


def parse_request(req: AccidentAnalysisRequest) -> Dict:
    """
    Turn raw input into normalized, structured core features.
    """
    features: Dict = {}

    features["seat_position"] = normalize_seat_position(req.seat_position)
    features["impact_side"] = normalize_impact_side(req.impact_side)
    features["estimated_speed_kmh"] = req.estimated_speed_kmh or 0.0

    features["has_injury_description"] = bool(req.injury_description)
    features["accident_description"] = req.accident_description.strip()
    features["injury_description"] = (req.injury_description or "").strip()
    features["has_dashcam"] = bool(req.dashcam_video_path)

    # Simple keywords that might matter later
    text = (req.accident_description + " " + (req.injury_description or "")).lower()
    features["mentions_rear_end"] = int("rear" in text and "hit" in text)
    features["mentions_side_impact"] = int("t-bone" in text or "side" in text)
    features["mentions_rollover"] = int("roll" in text)

    return features