from typing import Dict, Any


def generate_ai_summary(
    video_facts: Dict[str, Any],
    cohesion: Dict[str, Any],
    motion_sig: Dict[str, Any],
) -> str:
    label = video_facts.get("label", "unknown")
    score = cohesion.get("cohesion_score", 0)
    risk_peak = max(motion_sig.get("risk", [0.0])) if motion_sig.get("risk") else 0.0

    if label == "crash":
        return (
            f"Crash Lens flags this as a crash scenario with a clear risk spike "
            f"(peak {risk_peak:.2f}) and cohesion score {score}/100."
        )
    elif label == "normal":
        return (
            f"Crash Lens sees a low-risk, routine drive with cohesion score "
            f"{score}/100 and no major conflicts between sources."
        )
    else:
        return (
            f"Crash Lens processed this claim with cohesion score {score}/100; "
            f"evidence is limited, so treat the summary as indicative only."
        )
