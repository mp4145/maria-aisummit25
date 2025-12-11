from fastapi import FastAPI, HTTPException
from .routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

from .report import build_claim_report
from .video_loader import load_all_claims

BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="ClaimCinema API")

app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    index_path = FRONTEND_DIR / "templates" / "index.html"
    return index_path.read_text(encoding="utf-8")

@app.get("/api/claims")
def list_claims():
    claims = load_all_claims()
    return [
        {"claim_id": cid, "label": meta.get("label")}
        for cid, meta in claims.items()
    ]

@app.get("/api/claim/{claim_id}")
def get_claim(claim_id: str):
    try:
        report = build_claim_report(claim_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return report
