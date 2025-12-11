import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
VIDEOS_DIR = BASE_DIR / "data" / "videos"
ANNOT_DIR = BASE_DIR / "data" / "annotations"
META_DIR = BASE_DIR / "data" / "meta"
META_DIR.mkdir(parents=True, exist_ok=True)

CRASH_ANNOT_FILE = ANNOT_DIR / "Crash-1500.txt"
FPS = 10.0   # CCD videos are 50 frames @ 10 fps -> 5 seconds total

def load_crash_annotations():
    """
    Parse Crash-1500.txt into a dict:
    vidname -> {
        'event_frame_idx': int,
        'event_time_sec': float,
        'startframe': str,
        'youtube_id': str,
        'timing': str,
        'weather': str,
        'egoinvolve': bool
    }
    """
    crash_meta = {}
    if not CRASH_ANNOT_FILE.exists():
        print(f"Warning: {CRASH_ANNOT_FILE} not found, crash videos will have null metadata.")
        return crash_meta

    with CRASH_ANNOT_FILE.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Example line format:
            # 000001,[0,0,...,1,1],000285,0000,Day,Normal,Yes
            parts = line.split(",[")
            vidname = parts[0].strip()
            rest = "[%s" % parts[1]  # reconstruct the '[' we split off

            # Now split rest by "]," to separate binlabels from the rest
            binlabels_str, tail = rest.split("],", 1)
            binlabels_str = binlabels_str.strip()[1:]  # remove leading '['
            binlabels = [int(x.strip()) for x in binlabels_str.split(",")]

            tail_parts = tail.split(",")
            # According to the CCD README: startframe, youtubeID, timing, weather, egoinvolve
            startframe = tail_parts[0].strip()
            youtube_id = tail_parts[1].strip()
            timing = tail_parts[2].strip()
            weather = tail_parts[3].strip()
            egoinvolve_str = tail_parts[4].strip()
            egoinvolve = egoinvolve_str.lower() in ("yes", "true", "1")

            # event frame = index of first '1' (accident frame), or None if no 1
            event_frame_idx = None
            for i, v in enumerate(binlabels):
                if v == 1:
                    event_frame_idx = i
                    break

            event_time_sec = None
            if event_frame_idx is not None:
                event_time_sec = event_frame_idx / FPS

            crash_meta[vidname] = {
                "event_frame_idx": event_frame_idx,
                "event_time_sec": event_time_sec,
                "startframe": startframe,
                "youtube_id": youtube_id,
                "timing": timing,
                "weather": weather,
                "egoinvolve": egoinvolve
            }

    return crash_meta

def discover_videos():
    claims = {}
    crash_meta = load_crash_annotations()

    # Crash videos
    crash_dir = VIDEOS_DIR / "Crash-1500"
    if crash_dir.exists():
        for fname in sorted(crash_dir.iterdir()):
            if fname.suffix.lower() not in [".mp4", ".avi", ".mov"]:
                continue
            vidname = fname.stem  # e.g. "000001"
            claim_id = f"crash_{vidname}"

            meta = crash_meta.get(vidname, {})
            claims[claim_id] = {
                "claim_id": claim_id,
                "video_path": str(fname.relative_to(BASE_DIR)),
                "label": "crash",
                "event_frame_idx": meta.get("event_frame_idx"),
                "event_time_sec": meta.get("event_time_sec"),
                "startframe": meta.get("startframe"),
                "youtube_id": meta.get("youtube_id"),
                "timing": meta.get("timing"),
                "weather": meta.get("weather"),
                "egoinvolve": meta.get("egoinvolve")
            }

    # Normal videos (no Crash-1500.txt rows, so we leave event_time_sec None for now)
    normal_dir = VIDEOS_DIR / "Normal"
    if normal_dir.exists():
        for fname in sorted(normal_dir.iterdir()):
            if fname.suffix.lower() not in [".mp4", ".avi", ".mov"]:
                continue
            vidname = fname.stem
            claim_id = f"normal_{vidname}"
            claims[claim_id] = {
                "claim_id": claim_id,
                "video_path": str(fname.relative_to(BASE_DIR)),
                "label": "normal",
                "event_frame_idx": None,
                "event_time_sec": None,  # will be set to mid-clip later in loader
                "startframe": None,
                "youtube_id": None,
                "timing": None,
                "weather": None,
                "egoinvolve": None
            }

    return claims

def main():
    claims = discover_videos()
    out_path = META_DIR / "claims.json"
    with out_path.open("w") as f:
        json.dump(claims, f, indent=2)
    print(f"Wrote {len(claims)} claims to {out_path}")

if __name__ == "__main__":
    main()
