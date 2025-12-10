from typing import Dict, List
from ..models.model_clients import llm_client
from ..core.schemas import InjuryPattern, RiskScores


def heuristic_consistency_score(features: Dict) -> float:
    """
    Simple placeholder: high speed + has injury description + severe impact
    = higher consistency.
    """
    speed = features.get("estimated_speed_kmh", 0.0) or 0.0
    has_injury_desc = features.get("has_injury_description", False)
    severity = features.get("severity_score_heuristic", 0.0)

    score = 0.0
    if has_injury_desc:
        score += 30.0
    score += min(speed / 1.5, 40.0)
    score += min(severity / 2.0, 30.0)

    return max(0.0, min(score, 100.0))


def heuristic_fraud_risk(consistency_score: float) -> float:
    """
    Lower consistency = higher fraud risk.
    """
    return max(0.0, min(100.0 - consistency_score, 100.0))


def heuristic_injury_patterns(features: Dict) -> List[InjuryPattern]:
    impact_side = features.get("impact_side", "")
    seat = features.get("seat_position", "")

    patterns = []

    # Very simplified association rules
    if impact_side == "rear":
        patterns.append(InjuryPattern(body_region="neck", likelihood=0.85,
                                      notes="Whiplash is common in rear impacts."))
        patterns.append(InjuryPattern(body_region="upper back", likelihood=0.7))
    if impact_side in ["front", "rear"]:
        patterns.append(InjuryPattern(body_region="shoulders", likelihood=0.65))
    if impact_side in ["left", "right"]:
        patterns.append(InjuryPattern(body_region="side torso", likelihood=0.7))

    if not patterns:
        patterns.append(InjuryPattern(body_region="unspecified soft tissue", likelihood=0.4))

    return patterns


def build_llm_prompt(features: Dict) -> str:
    return f"""
You are an expert medical-legal accident analyst.

You are given structured accident features and (optional) injury description:

FEATURES:
{features}

Task:
1. Briefly assess the consistency between the accident dynamics and the injuries.
2. Highlight any red flags or mismatches that an insurer or attorney should investigate.
3. Suggest 3-5 follow-up questions for the patient or claimant.

Respond in plain English, 1-2 short paragraphs, then a numbered list of follow-up questions.
"""


def reason_about_injuries(features: Dict):
    # Heuristic scores first
    consistency = heuristic_consistency_score(features)
    fraud_risk = heuristic_fraud_risk(consistency)
    severity = features.get("severity_score_heuristic", 0.0)
    patterns = heuristic_injury_patterns(features)

    narrative = ""
    followups: List[str] = []

    if llm_client.is_configured():
        prompt = build_llm_prompt(features)
        llm_output = llm_client.generate(prompt)
        if llm_output:
            narrative = llm_output
            # simple split to approximate follow-ups
            parts = llm_output.split("\n")
            followups = [p.strip("- ").strip() for p in parts if p.strip().startswith((
                "1.", "2.", "3.", "4.", "5."
            ))]

    if not narrative:
        # fallback narrative
        narrative = (
            "Based on the reported impact, seating position, and speed, the claimed injuries "
            "appear moderately consistent with the accident dynamics. However, further clinical "
            "evaluation and documentation are required to confirm the full extent of injuries."
        )
    if not followups:
        followups = [
            "Can you describe when you first noticed the pain or symptoms?",
            "Were you wearing a seatbelt and how was your body positioned at impact?",
            "Have you had any prior injuries to the same areas?",
        ]

    risk_scores = RiskScores(
        consistency_score=round(consistency, 1),
        severity_score=round(severity, 1),
        fraud_risk_score=round(fraud_risk, 1),
    )

    return risk_scores, patterns, narrative, followups