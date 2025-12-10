# Accident Injury Triage Assistant (Agentic AI + CV on Dell Pro Max GB10)

## Overview

This project is an **agentic AI assistant for motor vehicle accidents**.

Given:
- accident description (time, location, speed, impact direction),
- seat position of each occupant (driver, front passenger, rear left/right/middle),
- optional dashcam video or image frames,

the system:
1. Uses **computer vision** to extract impact severity and scene context from dashcam media.
2. Uses an **LLM agent** to:
   - generate a structured **injury-likelihood profile** per occupant,
   - suggest **follow-up questions** for insurers / adjusters,
   - generate a **patient-facing narrative** they can attach to their claim.

It is designed to:
- **reduce cost** and friction for insurers,
- **improve accessibility** for patients who struggle to explain their injuries,
- run efficiently on **Dell Pro Max with GB10** using NVIDIA’s AI stack.

---

## Architecture

High-level components:

- `app/`
  - **FastAPI backend**
  - `/analyze_case` endpoint:
    - Inputs: JSON (crash details, seat positions) + optional media upload.
    - Pipeline:
      1. `cv_pipeline.py` (if media): run CV/VLM model (container on GB10), extract features:
         - estimated impact severity,
         - collision type (rear-end, side-impact, head-on),
         - rough timing of collision in video.
      2. `agent.py`: send a structured JSON with crash + CV features to an LLM endpoint (also on GB10).
      3. `scoring.py`: compute simple numeric scores:
         - risk per seat (0–1 or Low/Med/High),
         - flags (e.g. “delayed onset pain plausible”, “urgent ortho review suggested”).
      4. Return final JSON response.

- `ui/`
  - Simple **Streamlit** app:
    - form inputs for crash description and seat positions,
    - optional video/image upload,
    - displays:
      - per-seat risk cards,
      - insurer notes,
      - text for patient to copy.

- `data/demo/`
  - a few example JSON cases + short clips so judges can see it working even without internet.

---

## Requirements

- Python 3.10+
- Ubuntu (DGX OS on GB10)
- `pip` / `venv`
- Access to:
  - **NVIDIA model containers** running on GB10 (LLM + VLM/CV)
  - e.g. endpoints like:
    - `http://localhost:8001/vlm/infer`
    - `http://localhost:8002/llm/generate`

Python deps (in `requirements.txt`):

```txt
fastapi
uvicorn[standard]
pydantic
requests
streamlit
opencv-python
numpy