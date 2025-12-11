# Accident–Injury Consistency Assistant

An agentic AI API that helps evaluate **consistency between a motor vehicle accident (MVA) and the reported injuries**, for:

- **Insurers** – triage claims, flag obvious mismatches, highlight cases needing deeper review.
- **Attorneys & clinicians** – structured summaries of crash vs injury patterns.
- **Patients** – a plain-language explanation of how their symptoms may relate to the crash.

## Core Idea

Given:
- Accident metadata (speed, impact direction, vehicle size, etc.)
- Occupant position (driver / front passenger / rear left / rear right / rear middle)
- Claimed symptoms & timeline
- Optional dashcam-derived features

The system produces:
- A **consistency score** (0–1)
- A **predicted likely injury pattern & severity band**
- A **reasoned explanation** (for human review)
- A **structured report** for both patient and insurer views.

The MVP is implemented as a **FastAPI service** with a clean architecture and
is ready to be wired to NVIDIA / GB10–hosted LLMs and CV models.

## Quickstart (local dev)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn src.app.main_api:app --reload


DATA: https://drive.google.com/drive/folders/1Rx4LCo-9AbAdPw5Zh7wpKhMKLabZ5oA8