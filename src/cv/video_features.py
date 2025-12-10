import cv2

def extract_video_features(video_path: str):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    vehicle_like_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        if frame_count % 10 != 0:
            continue

        # TODO: swap this dummy with actual call to NVIDIA / YOLO detector
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        motion_proxy = gray.std()

        if motion_proxy > 40:  # arbitrary heuristic
            vehicle_like_frames += 1

    cap.release()

    relative_impact = vehicle_like_frames / max(frame_count, 1)

    return {
        "collision_detected": vehicle_like_frames > 0,
        "relative_impact": relative_impact,
        "total_frames": frame_count,
    }