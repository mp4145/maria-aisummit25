from typing import List, Optional
from pydantic import BaseModel, Field


# --- Input Schemas ---


class AccidentInfo(BaseModel):
    speed_mph: Optional[float] = Field(None, description="Approximate speed at impact.")
    impact_direction: Optional[str] = Field(
        None,
        description="front | rear | left_side | right_side | rollover | other",
    )
    collision_type: Optional[str] = Field(
        None,
        description="rear_end | head_on | side_impact | single_vehicle | multi_vehicle",
    )
    vehicle_mass_category: Optional[str] = Field(
        None,
        description="motorcycle | passenger_car | suv | pickup | truck | bus | other",
    )
    other_vehicle_mass_category: Optional[str] = None
    airbags_deployed: Optional[bool] = None
    seatbelts_used: Optional[bool] = None
    environment: Optional[str] = Field(
        None, description="e.g. dry_daylight, wet_night, snow, etc."
    )
    description_free_text: Optional[str] = Field(
        None, description="Optional narrative description of the crash."
    )


class OccupantInfo(BaseModel):
    position: str = Field(
        ...,
        description=(
            "driver | front_passenger | rear_left | rear_right | rear_middle"
        ),
    )
    age: Optional[int] = None
    sex: Optional[str] = Field(None, description="male | female | other")
    has_prior_neck_or_back_issues: Optional[bool] = None


class ClaimedInjuries(BaseModel):
    body_regions: List[str] = Field(
        ..., description="e.g. ['neck', 'right_shoulder', 'lower_back']"
    )
    onset_delay_days: Optional[int] = Field(
        None, description="Days from crash to initial symptom onset."
    )
    symptom_description: Optional[str] = None
    functional_limitations: Optional[str] = None
    medical_evaluations: Optional[str] = Field(
        None,
        description="Optional text: ER/urgent care visits, imaging, ortho notes.",
    )


class DashcamInfo(BaseModel):
    has_video: bool = False
    # For MVP: you can fill this manually or from a CV preprocessor
    impact_severity_bucket: Optional[str] = Field(
        None,
        description="low | moderate | high",
    )
    relative_impact_side: Optional[str] = Field(
        None, description="front | rear | left | right | unknown"
    )
    notes: Optional[str] = Field(
        None,
        description="Any notes from dashcam: number of impacts, multi-vehicle, etc.",
    )


class ClaimAnalysisRequest(BaseModel):
    accident: AccidentInfo
    occupant: OccupantInfo
    claimed_injuries: ClaimedInjuries
    dashcam_info: DashcamInfo = DashcamInfo()


# --- Output Schema ---


class ClaimAnalysisResponse(BaseModel):
    consistency_score: float = Field(
        ...,
        description="0–1, where 1 = highly consistent crash–injury pattern.",
    )
    expected_injury_profile: str
    consistency_explanation: str
    severity_band: str = Field(
        ...,
        description="e.g. low_soft_tissue, moderate_soft_tissue, high_severity_risk",
    )
    risk_flags: List[str]

    patient_summary: str
    insurer_summary: str