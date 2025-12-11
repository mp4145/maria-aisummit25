from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ClaimSummary(BaseModel):
  claim_id: str
  label: str


class MotionSignature(BaseModel):
  timestamps: List[float]
  risk: List[float]
  event_time_sec: Optional[float] = None


class ContradictionItem(BaseModel):
  fact: str
  status: str  # "support" | "conflict"


class CohesionReport(BaseModel):
  cohesion_score: int
  police_alignment: str
  contradictions: List[ContradictionItem]
  what_we_know: List[str]
  narrative_drift: str


class ClaimReport(BaseModel):
  claim_id: str
  motion_signature: MotionSignature
  cohesion: CohesionReport
  video_facts: Dict[str, Any]
  driver_statement: str
  police_summary: str
  ai_summary: str
  timings: Dict[str, float]
