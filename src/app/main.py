import streamlit as st
from pathlib import Path
from models.injury_model import load_injury_model, predict_injury_risk
from cv.video_features import extract_video_features
from agents.report_agent import generate_report

MODEL = None

def init_model():
    global MODEL
    if MODEL is None:
        MODEL = load_injury_model()

def main():
    st.title("CrashMap – AI Accident & Injury Consistency Agent")

    st.markdown(
        "Upload crash details and (optionally) a dashcam clip. "
        "The agent will estimate crash severity, likely injuries by seat, "
        "and generate a report for insurers and patients."
    )

    with st.form("crash_form"):
        col1, col2 = st.columns(2)
        with col1:
            impact_type = st.selectbox("Impact Type", ["rear-end", "side", "head-on", "multi-vehicle"])
            speed = st.slider("Approx speed at impact (mph)", 0, 120, 30)
            weather = st.selectbox("Weather", ["clear", "rain", "snow", "fog", "other"])
        with col2:
            seatbelt = st.selectbox("Seatbelts worn?", ["all", "some", "none", "unknown"])
            airbags = st.selectbox("Airbags deployed?", ["yes", "no", "unknown"])
            road_type = st.selectbox("Road type", ["highway", "city", "rural", "parking_lot"])

        description = st.text_area("Brief description (optional)")
        video_file = st.file_uploader("Optional dashcam video (short clip)", type=["mp4", "mov"])

        submitted = st.form_submit_button("Analyze")

    if submitted:
        init_model()

        crash_meta = {
            "impact_type": impact_type,
            "speed": speed,
            "weather": weather,
            "seatbelt": seatbelt,
            "airbags": airbags,
            "road_type": road_type,
            "description": description,
        }

        impact_features = None
        if video_file is not None:
            tmp_path = Path("data/raw/videos") / video_file.name
            tmp_path.parent.mkdir(parents=True, exist_ok=True)
            with open(tmp_path, "wb") as f:
                f.write(video_file.read())
            impact_features = extract_video_features(str(tmp_path))

        risk = predict_injury_risk(MODEL, crash_meta, impact_features)
        report = generate_report(crash_meta, risk, impact_features)

        st.subheader("Risk Assessment")
        st.json(risk)

        st.subheader("AI-Generated Report")
        st.write(report)

if __name__ == "__main__":
    main()