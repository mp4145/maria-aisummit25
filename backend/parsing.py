from typing import Dict, Any

def parse_driver_statement(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    facts = {}

    facts["pedestrian_present"] = "pedestrian" in text_lower and "did not" not in text_lower
    if "low speed" in text_lower:
        facts["speed_level"] = "low"
    elif "medium speed" in text_lower:
        facts["speed_level"] = "medium"
    elif "high speed" in text_lower:
        facts["speed_level"] = "high"

    # Very simple vehicle count guess
    if "about 1 vehicles" in text_lower or "not many other vehicles" in text_lower:
        facts["num_vehicles"] = 1
    elif "about 2 vehicles" in text_lower:
        facts["num_vehicles"] = 2
    elif "about 3 vehicles" in text_lower:
        facts["num_vehicles"] = 3

    return facts

def parse_police_summary(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    facts = {}

    facts["pedestrian_present"] = "pedestrians were present" in text_lower
    if "no pedestrians" in text_lower:
        facts["pedestrian_present"] = False

    if "approximately" in text_lower and "vehicles" in text_lower:
        # crude extract: "approximately X vehicles"
        try:
            idx = text_lower.split("approximately")[1].split("vehicles")[0]
            num = int("".join(ch for ch in idx if ch.isdigit()))
            facts["num_vehicles"] = num
        except Exception:
            pass

    if "ego vehicle appears to be involved" in text_lower:
        facts["egoinvolve"] = True
    elif "does not appear to be directly involved" in text_lower:
        facts["egoinvolve"] = False

    return facts
