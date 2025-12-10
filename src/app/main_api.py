from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.schemas import ClaimAnalysisRequest, ClaimAnalysisResponse
from src.services.accident_parser import parse_accident_input
from src.services.video_processor import process_dashcam_info
from src.services.feature_builder import build_feature_vector
from src.services.injury_reasoner import reason_about_injuries
from src.services.report_generator import generate_reports

app = FastAPI(
    title="Accident–Injury Consistency Assistant",
    description="Agentic AI service to evaluate consistency between car accidents and reported injuries.",
    version="0.1.0",
)

# CORS (so you can later add a web UI if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze-claim", response_model=ClaimAnalysisResponse)
def analyze_claim(payload: ClaimAnalysisRequest):
    """
    Main endpoint:
    1. Parse accident + occupant + injuries + optional dashcam info
    2. Build feature vector
    3. Run injury reasoning (rule + optional LLM)
    4. Generate patient + insurer reports
    """
    accident_features = parse_accident_input(payload.accident, payload.occupant)
    dashcam_features = process_dashcam_info(payload.dashcam_info)

    features = build_feature_vector(
        accident_features=accident_features,
        dashcam_features=dashcam_features,
        claimed_injuries=payload.claimed_injuries,
    )

    reasoning_result = reason_about_injuries(features)
    reports = generate_reports(features, reasoning_result)

    return ClaimAnalysisResponse(
        **reasoning_result,
        **reports,
    )