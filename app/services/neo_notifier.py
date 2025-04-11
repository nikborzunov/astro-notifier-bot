# app/services/neo_notifier.py

import logging
from app.services.notifications import send_notification
from app.services.nasa_data import get_near_earth_objects
from app.db.database import insert_neo, insert_neo_history

logger = logging.getLogger(__name__)

async def fetch_and_notify_neo():
    try:
        neo_data = await get_near_earth_objects()
        if neo_data:
            for neo in neo_data:
                name = neo["name"]
                diameter = neo["estimated_diameter"]["meters"]["estimated_diameter_max"]
                hazardous = neo["is_potentially_hazardous_asteroid"]
                discovery_date = neo["discovery_date"]
                insert_neo(name, diameter, hazardous, discovery_date)
                insert_neo_history(name, diameter, hazardous, discovery_date)
                
                if hazardous:
                    send_notification(f"Potentially hazardous asteroid: {name} - Diameter: {diameter} meters")
    except Exception as e:
        logger.error(f"Error fetching and notifying NEOs: {e}")
