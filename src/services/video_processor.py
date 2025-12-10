from typing import Dict, Any
from src.core.schemas import DashcamInfo


def process_dashcam_info(info: DashcamInfo) -> Dict[str, Any]:
    """
    MVP: Just pass through structured dashcam-derived attributes.

    Later, this is where you:
    - Extract frames from dashcam video
    - Run CV (e.g. object detection, collision severity estimation)
    - Derive impact side & severity buckets using NVIDIA CV models on GB10.
    """
    features: Dict[str, Any] = {
        "has_video": info.has_video,
        "impact_severity_bucket": info.impact_severity_bucket or "unknown",
        "relative_impact_side": info.relative_impact_side or "unknown",
        "dashcam_notes": info.notes or "",
    }
    return features