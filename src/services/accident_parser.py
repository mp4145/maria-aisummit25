from typing import Dict, Any
from src.core.schemas import AccidentInfo, OccupantInfo


def parse_accident_input(accident: AccidentInfo, occupant: OccupantInfo) -> Dict[str, Any]:
    """
    Convert input into a normalized feature dict.
    This is where you would eventually join with real accident/injury datasets
    to learn better priors and risk factors.
    """
    features: Dict[str, Any] = {}

    # Basic numeric features
    features["speed_mph"] = accident.speed_mph or 0.0

    # One-hot-ish categorical encodings (simple strings for MVP)
    features["impact_direction"] = accident.impact_direction or "unknown"
    features["collision_type"] = accident.collision_type or "unknown"
    features["vehicle_mass_category"] = accident.vehicle_mass_category or "unknown"
    features["other_vehicle_mass_category"] = (
        accident.other_vehicle_mass_category or "unknown"
    )

    features["airbags_deployed"] = bool(accident.airbags_deployed)
    features["seatbelts_used"] = bool(accident.seatbelts_used)
    features["environment"] = accident.environment or "unknown"

    # Occupant-related
    features["occupant_position"] = occupant.position
    features["occupant_age"] = occupant.age or 0
    features["occupant_sex"] = occupant.sex or "unknown"
    features["prior_neck_or_back_issues"] = bool(
        occupant.has_prior_neck_or_back_issues
    )

    # Free text description kept for LLM context (later)
    features["accident_description_text"] = accident.description_free_text or ""

    return features