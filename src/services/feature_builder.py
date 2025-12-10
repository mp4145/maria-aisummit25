from typing import Dict


def compute_basic_severity(features: Dict) -> float:
    """
    Very rough heuristic for severity based on speed, impact, seat position.
    """
    speed = features.get("estimated_speed_kmh", 0.0) or 0.0
    impact_side = features.get("impact_side", "")
    seat = features.get("seat_position", "")

    base = min(speed / 2.0, 50.0)  # cap

    if impact_side in ["rear", "front"]:
        base += 10.0
    if impact_side in ["left", "right"]:
        base += 15.0  # side impacts often more risky

    if seat in ["rear_center", "rear_left", "rear_right"]:
        base += 5.0  # often less protected or variable seatbelt use

    return max(0.0, min(base, 100.0))


def merge_features(parsed: Dict, video_feats: Dict) -> Dict:
    merged = {**parsed, **video_feats}
    merged["severity_score_heuristic"] = compute_basic_severity(merged)
    return merged