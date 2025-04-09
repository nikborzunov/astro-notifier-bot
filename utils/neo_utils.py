# utils/neo_utils.py

from datetime import datetime

def get_approach_date(neo):
    try:
        return datetime.strptime(neo["close_approach_data"][0]["close_approach_date"], "%Y-%m-%d")
    except:
        return datetime.min

def get_diameter(neo):
    try:
        return float(neo["estimated_diameter"]["meters"]["estimated_diameter_max"])
    except (KeyError, ValueError):
        return 0

def get_value_from_neo(neo, *keys):
    try:
        value = neo
        for key in keys:
            if isinstance(value, list):
                if key == 0 and value:
                    value = value[0]
                else:
                    value = "Unknown"
            else:
                value = value.get(key, "Unknown")
        return value if value != "Unknown" else "Data not available"
    except (KeyError, IndexError):
        return "Data not available"

def build_neo_message(top_3_neo):
    message = (
        "🌌 **Top 3 Potentially Hazardous NEOs in the Last 7 Days** 🚀\n\n"
        "Here are the details of the 3 largest potentially hazardous Near-Earth Objects (NEOs) observed in the last 7 days.\n\n"
        "🔭 **Details on each NEO:**\n\n"
    )

    for neo in top_3_neo:
        neo_name = get_value_from_neo(neo, "name")
        neo_diameter = get_value_from_neo(neo, "estimated_diameter", "meters", "estimated_diameter_max")
        neo_velocity = get_value_from_neo(neo, "close_approach_data", 0, "relative_velocity", "kilometers_per_hour")
        neo_approach_date = get_value_from_neo(neo, "close_approach_data", 0, "close_approach_date")
        neo_min_distance = get_value_from_neo(neo, "close_approach_data", 0, "miss_distance", "kilometers")

        message += (
            f"🪐 **{neo_name}** \n"
            f"🌌 **Size**: {neo_diameter} m\n"
            f"⚡ **Speed**: {neo_velocity}\n"
            f"📅 **Closest Approach**: {neo_approach_date}\n"
            f"🌍 **Min Distance**: {neo_min_distance}\n"
            "\n━━━━━━━━━━━━━━━━━━━━━\n"
        )

    message += "\nStay curious and safe! 🌌💫"
    return message
