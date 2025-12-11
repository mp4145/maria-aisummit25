# backend/cohesion.py
from typing import Dict, Any, List

def compute_cohesion_report(video_facts: Dict[str, Any]) -> Dict[str, Any]:
    label = video_facts.get("label", "unknown")
    speed_level = video_facts.get("speed_level", "unknown")
    num_vehicles = video_facts.get("num_vehicles") or 0

    if label == "normal":
        # Base
        cohesion_score = 85
        police_alignment = "high"
        contradictions: List[Dict[str, str]] = []
        what_we_know = ["Video and statements are broadly consistent."]

        # Adjust slightly by scene complexity
        if num_vehicles > 2:
            cohesion_score -= 5
            what_we_know.append("Traffic density is slightly elevated.")
        if speed_level == "high":
            cohesion_score -= 5
            what_we_know.append("Driver reports higher speed, but no incident is visible.")

        narrative_drift = "No significant drift detected."
    elif label == "crash":
        cohesion_score = 60
        police_alignment = "medium"
        contradictions = [{"fact": "speed", "status": "conflict"}]
        what_we_know = ["Crash occurred with some discrepancy in reported speed."]

        if num_vehicles > 2:
            what_we_know.append("Multiple vehicles appear near the impact.")
        if speed_level == "low":
            contradictions.append({"fact": "impact_severity", "status": "conflict"})

        narrative_drift = "Driver narrative softens responsibility over time."
    else:
        cohesion_score = 70
        police_alignment = "unknown"
        contradictions = []
        what_we_know = ["Insufficient data for a strong cohesion estimate."]
        narrative_drift = "Not enough signal to assess narrative drift."

    return {
        "cohesion_score": cohesion_score,
        "police_alignment": police_alignment,
        "contradictions": contradictions,
        "what_we_know": what_we_know,
        "narrative_drift": narrative_drift,
    }
