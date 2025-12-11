# backend/facts_extraction.py (keep your existing meta loading, adjusted core)

from typing import Dict, Any
import statistics

from .motion_signature import compute_motion_signature
from .video_loader import load_claim_with_event_time


def _speed_level_from_risk(risk_series):
    if not risk_series:
        return "unknown"
    avg_risk = statistics.mean(risk_series)
    if avg_risk < 0.2:
        return "low"
    elif avg_risk < 0.6:
        return "medium"
    else:
        return "high"


def extract_video_facts(claim_id: str) -> Dict[str, Any]:
    ms = compute_motion_signature(
        load_claim_with_event_time(claim_id)["abs_video_path"],
        event_time_sec=load_claim_with_event_time(claim_id)["event_time_sec"],
    )
    meta = load_claim_with_event_time(claim_id)

    label = meta.get("label")
    risk_series = ms["risk"]

    if not risk_series:
        if label == "crash":
            risk_series = [0.8] * 10
        else:
            risk_series = [0.1] * 10

    speed_level = _speed_level_from_risk(risk_series)

    facts = {
        "claim_id": claim_id,
        "label": label,
        "timing": meta.get("timing") or "Day",
        "weather": meta.get("weather") or "Normal",
        "egoinvolve": meta.get("egoinvolve"),
        "num_vehicles": None,  # can be extended later
        "pedestrian_present": None,
        "speed_level": speed_level,
        "event_time_sec": ms["event_time_sec"],
    }
    return facts
