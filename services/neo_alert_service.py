from data.database import insert_neo
from services.notifications import send_notification
from services.nasa_api import get_near_earth_objects

def fetch_and_notify_neo():
    neo_data = get_near_earth_objects()
    if neo_data:
        for neo in neo_data:
            name = neo["name"]
            diameter = neo["estimated_diameter"]["meters"]["estimated_diameter_max"]
            hazardous = neo["is_potentially_hazardous_asteroid"]
            insert_neo(name, diameter, hazardous)
            if hazardous:
                send_notification(f"Potentially hazardous asteroid: {name} - Diameter: {diameter} meters")