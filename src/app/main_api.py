from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..core.config import settings
from ..core.schemas import AccidentAnalysisRequest, AccidentAnalysisResponse
from ..services.accident_parser import parse_request
from ..services.video_processor import analyze_dashcam_video
from ..services.feature_builder import merge_features
from ..services.injury_reasoner import reason_about_injuries
from ..services.report_generator import build_response

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze", response_model=AccidentAnalysisResponse)
def analyze_accident(payload: AccidentAnalysisRequest):
    parsed = parse_request(payload)
    video_feats = analyze_dashcam_video(payload.dashcam_video_path)
    merged_feats = merge_features(parsed, video_feats)
    scores, patterns, narrative, followups = reason_about_injuries(merged_feats)
    response = build_response(merged_feats, scores, patterns, narrative, followups)
    return response