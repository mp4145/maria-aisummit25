import streamlit as st
import requests

API_URL = "http://localhost:8000/analyze"


def main():
    st.title("Accident-to-Injury Consistency AI (Demo)")

    accident_description = st.text_area("Accident Description", height=150)
    injury_description = st.text_area("Injury Description (optional)", height=100)

    seat_position = st.selectbox(
        "Seat Position",
        ["driver", "front_passenger", "rear_left", "rear_right", "rear_center"],
    )
    impact_side = st.selectbox(
        "Impact Side",
        ["front", "rear", "left", "right", "rollover", "multi"],
    )
    estimated_speed_kmh = st.number_input("Estimated Speed (km/h)", min_value=0.0, max_value=200.0, value=30.0)
    dashcam_video_path = st.text_input("Dashcam video path (optional)", "")

    if st.button("Analyze"):
        payload = {
            "accident_description": accident_description,
            "seat_position": seat_position,
            "impact_side": impact_side,
            "estimated_speed_kmh": estimated_speed_kmh,
            "injury_description": injury_description or None,
            "dashcam_video_path": dashcam_video_path or None,
        }
        try:
            resp = requests.post(API_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()

            st.subheader("Risk Scores")
            st.write(data["risk_scores"])

            st.subheader("Likely Injuries")
            for inj in data["likely_injuries"]:
                st.write(f"- {inj['body_region']} (likelihood {inj['likelihood']*100:.0f}%)")

            st.subheader("Key Factors")
            for k in data["key_factors"]:
                st.write(f"- {k}")

            st.subheader("Narrative Summary")
            st.write(data["narrative_summary"])

            st.subheader("Suggested Follow-ups")
            for q in data["suggested_followups"]:
                st.write(f"- {q}")

        except Exception as e:
            st.error(f"Error calling API: {e}")


if __name__ == "__main__":
    main()