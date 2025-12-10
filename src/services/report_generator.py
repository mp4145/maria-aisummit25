from typing import Dict, Any


def generate_reports(
    features: Dict[str, Any],
    reasoning_result: Dict[str, Any],
) -> Dict[str, str]:
    """
    Create two narrative views:
      - patient_summary
      - insurer_summary
    """
    score = reasoning_result["consistency_score"]
    severity_band = reasoning_result["severity_band"]
    expected_profile = reasoning_result["expected_injury_profile"]

    onset_delay = int(features.get("onset_delay_days", 0))
    speed = float(features.get("speed_mph", 0.0))
    impact_direction = features.get("impact_direction", "unknown")
    occupant_position = features.get("occupant_position", "unknown")
    body_regions = ", ".join(features.get("claimed_body_regions", []))

    patient_summary = (
        f"Based on the crash description (about {speed:.0f} mph, "
        f"{impact_direction.replace('_', ' ')} impact) and your seat position "
        f"({occupant_position.replace('_', ' ')}), injuries affecting {body_regions} "
        f"are considered {severity_band.replace('_', ' ')} from a medical and biomechanical "
        f"perspective. Your symptoms starting around day {onset_delay} are not unusual for "
        f"this type of event. This tool does not replace a doctor, but is meant to help "
        f"organize the information for you and your care team."
    )

    insurer_summary = (
        f"Crash parameters: approx {speed:.0f} mph, {impact_direction} impact, "
        f"occupant position {occupant_position}, claimed regions: {body_regions}, "
        f"onset delay {onset_delay} days. The heuristic consistency score is {score:.2f} "
        f"with a severity band of '{severity_band}'. Expected profile: {expected_profile} "
        f"Automated risk flags: {reasoning_result['risk_flags']}. "
        f"This output is intended as a triage aid, not a final adjudication. "
    )

    return {
        "patient_summary": patient_summary,
        "insurer_summary": insurer_summary,
    }
