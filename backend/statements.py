from typing import Dict, Any


def _safe_lower(value: Any, default: str) -> str:
    if value is None:
        return default.lower()
    try:
        return str(value).lower()
    except Exception:
        return default.lower()


def generate_driver_statement(facts: Dict[str, Any]) -> str:
    label = facts.get("label")
    timing = _safe_lower(facts.get("timing", "Unknown"), "Unknown")
    weather = _safe_lower(facts.get("weather", "Unknown"), "Unknown")
    num_vehicles = facts.get("num_vehicles")
    speed_level = facts.get("speed_level", "unknown")
    ped = facts.get("pedestrian_present", False)

    # Safe defaults
    if num_vehicles is None:
        num_vehicles = 0

    if label == "normal":
        base = "I was driving normally"
    else:
        base = "I was driving when there was a crash"

    if timing != "unknown":
        base += f" during the {timing}"
    if weather != "unknown":
        base += f" in {weather} conditions"

    if num_vehicles > 1:
        base += f", and there were about {num_vehicles} vehicles around"
    else:
        base += ", and there were not many other vehicles around"

    if ped:
        base += ". I did notice pedestrians nearby."
    else:
        base += ". I did not see any pedestrians."

    if speed_level != "unknown":
        base += f" I was going at roughly {speed_level} speed."

    return base + "."


def generate_police_summary(facts: Dict[str, Any]) -> str:
    label = facts.get("label")
    timing_raw = facts.get("timing", "Unknown")
    weather_raw = facts.get("weather", "Unknown")
    timing = _safe_lower(timing_raw, "Unknown")
    weather = _safe_lower(weather_raw, "Unknown")
    num_vehicles = facts.get("num_vehicles", 0)
    ped = facts.get("pedestrian_present", False)
    egoinvolve = facts.get("egoinvolve")

    if num_vehicles is None:
        num_vehicles = 0

    if label == "normal":
        base = "No collision was recorded in this clip."
    else:
        base = "A collision was recorded in this clip."

    if timing_raw not in (None, "Unknown"):
        base += f" The incident occurred during the {timing}."
    if weather_raw not in (None, "Unknown"):
        base += f" Weather conditions were {weather}."

    base += f" Approximately {num_vehicles} vehicles were visible."

    if ped:
        base += " Pedestrians were present in the scene."
    else:
        base += " No pedestrians were clearly visible."

    if egoinvolve is True:
        base += " The ego vehicle appears to be involved."
    elif egoinvolve is False:
        base += " The ego vehicle does not appear to be directly involved."

    return base + "."


def generate_statements(facts: Dict[str, Any]) -> Dict[str, str]:
    return {
        "driver_statement": generate_driver_statement(facts),
        "police_summary": generate_police_summary(facts),
    }
