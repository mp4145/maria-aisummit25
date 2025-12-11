# Components

- **Backend API (FastAPI)**: Serves claim list and visual intelligence reports under `/api`.
- **Detector (ONNX/YOLO slot)**: Single object detection model used to derive motion signature and scene facts.
- **Motion Signature**: Pure-Python risk-over-time curve computed from detector outputs.
- **Evidence Cohesion Engine**: Rule-based comparison of driver and police narratives to compute cohesion, contradictions, and drift.
- **Frontend Dashboard**: Minimal HTML + Chart.js single-page dashboard for visualizing risk curve and evidence map.
- **GB10 Deployment**: Same code, different script (`run_gb10.sh`) and CUDA-enabled OpenCV build.
