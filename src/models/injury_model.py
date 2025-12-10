import json
import numpy as np

# For hackathon, you can start with heuristic model,
# then swap with a trained one once ready.

def load_injury_model():
    # Later: load a real model from `models/weights/`
    return {"version": "0.1", "type": "heuristic"}

def predict_injury_risk(model, crash_meta, impact_features=None):
    base = crash_meta["speed"]
    if crash_meta["impact_type"] == "head-on":
        base += 20
    if crash_meta["impact_type"] == "side":
        base += 10

    if crash_meta["seatbelt"] in ["none", "some"]:
        base += 15

    if impact_features and impact_features.get("collision_detected"):
        base += 10 * impact_features.get("relative_impact", 1.0)

    score = min(base / 100.0, 1.0)
    severity = "low"
    if score > 0.7:
        severity = "high"
    elif score > 0.4:
        severity = "medium"

    return {
        "injury_risk_score": float(score),
        "injury_severity_class": severity,
        "details": {
            "meta": crash_meta,
            "impact_features": impact_features,
        },
    }