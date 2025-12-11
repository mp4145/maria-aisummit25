# backend/routes.py

from fastapi import APIRouter
from .video_loader import load_all_claims
from .report import build_claim_report
from .schemas import ClaimSummary, ClaimReport


router = APIRouter()


@router.get("/claims", response_model=list[ClaimSummary])
async def list_claims():
    """
    Return all available claim IDs for the dropdown.
    load_all_claims() returns a list of strings like:
      ["crash_000001", "normal_000002", ...]
    """
    claim_ids = load_all_claims()

    def _label_from_id(cid: str) -> str:
        if cid.startswith("crash_"):
            return "crash"
        if cid.startswith("normal_"):
            return "normal"
        return "unknown"

    return [ClaimSummary(claim_id=c, label=_label_from_id(c)) for c in claim_ids]


@router.get("/claim/{claim_id}", response_model=ClaimReport)
async def get_claim_report(claim_id: str):
    """
    Build and return the full visual intelligence report for a single claim.
    build_claim_report(claim_id) is responsible for loading any
    video facts and computing motion/cohesion internally.
    """
    report_dict = build_claim_report(claim_id)
    return ClaimReport(**report_dict)
