from typing import Dict, Any, List
from src.models.model_clients import call_llm


def _estimate_base_severity(features: Dict[str, Any]) -> str:
    """
    Simple rule-of-thumb banding for severity based on speed and impact.

    low_soft_tissue | moderate_soft_tissue | high_severity_risk
    """
    speed = float(features.get("speed_mph", 0.0))
    impact_dir = features.get("impact_direction", "unknown")
    impact_bucket = features.get("dashcam_impact_severity_bucket", "unknown")

    # Very naive rules – you can refine this using real datasets later.
    if impact_bucket == "high" or speed >= 45:
        return "high_severity_risk"
    if impact_bucket == "moderate" or 20 <= speed < 45:
        return "moderate_soft_tissue"
    return "low_soft_tissue"


def _rough_consistency_score(features: Dict[str, Any]) -> float:
    """
    Rough, explainable heuristic that you can refine later.
    """
    speed = float(features.get("speed_mph", 0.0))
    onset_delay = int(features.get("onset_delay_days", 0))
    regions = [r.lower() for r in features.get("claimed_body_regions", [])]
    impact_direction = features.get("impact_direction", "unknown")
    occupant_position = features.get("occupant_position", "unknown")

    score = 0.5  # start neutral

    # Speed contribution
    if speed < 5:
        score -= 0.15
    elif speed < 15:
        score -= 0.05
    elif 15 <= speed <= 40:
        score += 0.1
    else:
        score += 0.2

    # Delayed onset: 0–3 days plausible, 4–10 days borderline, >10 days questionable
    if onset_delay <= 3:
        score += 0.05
    elif onset_delay <= 10:
        score += 0.0
    else:
        score -= 0.1

    # Simple biomechanical mapping:
    if impact_direction == "rear" and "neck" in regions:
        score += 0.1
    if impact_direction in ("left_side", "right_side"):
        if occupant_position == "driver" and "left" in " ".join(regions):
            score += 0.05
        if occupant_position == "front_passenger" and "right" in " ".join(regions):
            score += 0.05

    # Clamp to [0, 1]
    score = max(0.0, min(1.0, score))
    return round(score, 2)


def reason_about_injuries(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main reasoning function.

    Uses:
      - Simple heuristic scoring
      - LLM call (optional / stub) for natural language reasoning
    """
    severity_band = _estimate_base_severity(features)
    consistency_score = _rough_consistency_score(features)

    body_regions = features.get("claimed_body_regions", [])
    onset_delay = features.get("onset_delay_days", 0)
    speed = features.get("speed_mph", 0.0)
    impact_direction = features.get("impact_direction", "unknown")
    occupant_position = features.get("occupant_position", "unknown")

    expected_profile = (
        f"Likely soft-tissue / whiplash-type injury involving {', '.join(body_regions)}."
        if severity_band != "high_severity_risk"
        else "Crash parameters suggest a non-trivial risk of more serious injury; advanced imaging and close follow-up warranted."
    )

    risk_flags: List[str] = []

    if speed < 5 and severity_band != "high_severity_risk":
        risk_flags.append(
            "Very low apparent speed – consider vehicle damage photos, dashcam, and prior history."
        )

    if onset_delay > 10:
        risk_flags.append(
            "Symptom onset reported >10 days after crash – still possible but requires careful clinical correlation."
        )

    if impact_direction == "rear" and "neck" not in [r.lower() for r in body_regions]:
        risk_flags.append(
            "Rear-end collisions often involve neck complaints; absence may be benign or underreported."
        )

    # LLM-based explanation stub (later you plug GB10 model here)
    llm_prompt = (
        "You are a medico-legal assistant. Given the following crash and injury features, "
        "explain in a balanced, neutral way whether the reported injuries are consistent "
        "with the described accident:\n\n"
        f"{features}\n\n"
        "Respond in 3–4 sentences, focusing on clinical plausibility, biomechanics, and "
        "any caveats that require human review."
    )
    llm_explanation = call_llm(llm_prompt)

    # For hackathon demo, we mainly need the fields below:
    return {
        "consistency_score": consistency_score,
        "expected_injury_profile": expected_profile,
        "consistency_explanation": llm_explanation,
        "severity_band": severity_band,
        "risk_flags": risk_flags,
    }