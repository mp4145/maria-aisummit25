from typing import Dict, Any
from src.core.schemas import ClaimedInjuries


def build_feature_vector(
    accident_features: Dict[str, Any],
    dashcam_features: Dict[str, Any],
    claimed_injuries: ClaimedInjuries,
) -> Dict[str, Any]:
    """
    Combines accident + dashcam + claimed injuries into a single feature dict.
    """
    features: Dict[str, Any] = {}

    # Merge accident & dashcam
    features.update(accident_features)
    features.update({f"dashcam_{k}": v for k, v in dashcam_features.items()})

    # Injuries
    features["claimed_body_regions"] = claimed_injuries.body_regions
    features["onset_delay_days"] = claimed_injuries.onset_delay_days or 0
    features["symptom_description"] = claimed_injuries.symptom_description or ""
    features["functional_limitations"] = (
        claimed_injuries.functional_limitations or ""
    )
    features["medical_evaluations"] = claimed_injuries.medical_evaluations or ""

    return features