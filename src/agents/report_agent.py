import textwrap
# Later: import NVIDIA / Spark LLM client

def generate_report(crash_meta, risk, impact_features):
    # For now, simple templated text. Later, replace with LLM call.
    severity = risk["injury_severity_class"]
    score = risk["injury_risk_score"]

    video_line = "No dashcam video was provided."
    if impact_features:
        if impact_features.get("collision_detected"):
            video_line = "Dashcam evidence suggests a meaningful collision event."
        else:
            video_line = "Dashcam evidence does not clearly show a collision."

    report = f"""
    Summary:
    - Estimated injury risk: {severity.upper()} (score {score:.2f})
    - Impact type: {crash_meta['impact_type']} at ~{crash_meta['speed']} mph
    - Safety context: seatbelts = {crash_meta['seatbelt']}, airbags = {crash_meta['airbags']}
    - Conditions: weather = {crash_meta['weather']}, road = {crash_meta['road_type']}

    Evidence from video:
    - {video_line}

    Interpretation for insurers:
    - The crash profile and conditions are {severity} risk for clinically significant injuries.
    - This tool is designed as a triage/decision-support system, not to automatically deny claims.

    Interpretation for patients:
    - Given the crash type and severity, symptoms affecting the neck, shoulders or back may develop 
      hours to days after the event and can still be consistent with injury from this crash.
    - Follow-up with orthopedics/physio and proper documentation will strengthen the case.

    Next steps:
    - Collect and attach radiology, specialist reports, and PT notes where applicable.
    - For borderline cases, request additional medical review instead of outright denial.
    """
    return textwrap.dedent(report).strip()