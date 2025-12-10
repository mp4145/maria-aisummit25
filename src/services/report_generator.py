from typing import Dict, List
from ..core.schemas import AccidentAnalysisResponse, RiskScores, InjuryPattern


def extract_key_factors(features: Dict, scores: RiskScores) -> List[str]:
    factors = []

    if features.get("estimated_speed_kmh", 0) >= 40:
        factors.append("Moderate to high impact speed.")
    if features.get("impact_side") == "rear":
        factors.append("Rear-end collision – whiplash-type injuries plausible.")
    if features.get("has_injury_description"):
        factors.append("Claimant provided a detailed injury description.")
    if scores.fraud_risk_score > 60:
        factors.append("Low accident-to-injury consistency – elevated fraud risk.")

    return factors


def build_response(
    features: Dict,
    scores: RiskScores,
    patterns: List[InjuryPattern],
    narrative: str,
    followups: List[str],
) -> AccidentAnalysisResponse:
    key_factors = extract_key_factors(features, scores)

    return AccidentAnalysisResponse(
        risk_scores=scores,
        likely_injuries=patterns,
        key_factors=key_factors,
        narrative_summary=narrative,
        suggested_followups=followups,
        raw_features={k: str(v) for k, v in features.items()},
    )