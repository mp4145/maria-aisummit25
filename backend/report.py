from pathlib import Path
from typing import Dict, Any

from .motion_signature import compute_motion_signature
from .video_loader import load_claim_with_event_time
from .cohesion import compute_cohesion_report
from .summary import generate_ai_summary
from .facts_extraction import extract_video_facts

DATA_ROOT = Path("data/videos")


def _video_path_from_claim_id(claim_id: str) -> Path:
    """
    crash_000001 -> data/videos/Crash-1500/000001.mp4
    normal_000001 -> data/videos/Normal/000001.mp4
    """
    prefix, num = claim_id.split("_", 1)
    if prefix.lower() == "crash":
        folder = "Crash-1500"
    else:
        folder = "Normal"
    return DATA_ROOT / folder / f"{num}.mp4"


def build_claim_report(claim_id: str) -> Dict[str, Any]:
    # whatever your loader returns; handle 2 or 3 tuple shapes
    result = load_claim_with_event_time(claim_id)

    if isinstance(result, tuple):
        if len(result) == 2:
            video_meta, event_time = result
        elif len(result) == 3:
            _, video_meta, event_time = result
        else:
            video_meta, event_time = result[0], result[-1]
    else:
        video_meta, event_time = result, None

    # base facts from metadata + id
    video_facts = extract_video_facts(claim_id)
    if isinstance(video_meta, dict):
        video_facts.update(video_meta)

    from .statements import generate_statements

    statements = generate_statements(video_facts)
    driver_statement = statements["driver_statement"]
    police_summary = statements["police_summary"]

    video_path = _video_path_from_claim_id(claim_id)
    motion_sig = compute_motion_signature(str(video_path), event_time_sec=event_time)
    cohesion = compute_cohesion_report(video_facts)
    ai_summary = generate_ai_summary(video_facts, cohesion, motion_sig)

    return {
    "claim_id": claim_id,
    "motion_signature": motion_sig,
    "cohesion": cohesion,
    "video_facts": video_facts,
    "driver_statement": driver_statement,
    "police_summary": police_summary,
    "ai_summary": ai_summary,
    "timings": {},
}
