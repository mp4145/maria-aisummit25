from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class AccidentAnalysisRequest(BaseModel):
    accident_description: str = Field(..., description="Narrative of how the accident happened")
    seat_position: str = Field(..., description="driver | front_passenger | rear_left | rear_right | rear_center")
    impact_side: str = Field(..., description="front | rear | left | right | rollover | multi")
    estimated_speed_kmh: Optional[float] = Field(None, description="Approximate speed at time of impact")
    injury_description: Optional[str] = Field(None, description="Claimed injuries / symptoms")
    dashcam_video_path: Optional[str] = Field(None, description="Optional path to dashcam video (on system)")


class RiskScores(BaseModel):
    consistency_score: float
    severity_score: float
    fraud_risk_score: float


class InjuryPattern(BaseModel):
    body_region: str
    likelihood: float
    notes: Optional[str] = None


class AccidentAnalysisResponse(BaseModel):
    risk_scores: RiskScores
    likely_injuries: List[InjuryPattern]
    key_factors: List[str]
    narrative_summary: str
    suggested_followups: List[str]
    raw_features: Dict[str, str]