from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from services.nasa_api import get_apod, get_near_earth_objects
from data.database import insert_apod, insert_neo
from services.notifications import send_notification
import os

logger = logging.getLogger(__name__)

# Function to fetch and process data
def scheduled_task():
    try:
        # Fetch Astronomy Picture of the Day (APOD)
        apod_data = get_apod()
        if apod_data:
            title = apod_data["title"]
            url = apod_data["url"]
            date = apod_data["date"]
            insert_apod(title, url, date)  # Save to database
            send_notification(f"Today's APOD: {title} - {url}")
        
        # Fetch Near-Earth Objects (NEO)
        neo_data = get_near_earth_objects()
        if neo_data:
            for neo in neo_data:
                name = neo["name"]
                diameter = neo["estimated_diameter"]["meters"]["estimated_diameter_max"]
                hazardous = neo["is_potentially_hazardous_asteroid"]
                insert_neo(name, diameter, hazardous)  # Save to database
                send_notification(f"Potentially hazardous asteroid: {name} - Diameter: {diameter} meters")
    except Exception as e:
        logger.error(f"Error in scheduled task: {e}")

# Function to start the scheduler
def start_scheduler():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            scheduled_task, 
            IntervalTrigger(seconds=3600),  # Task will run every 1 hour
            id='space_data_task',
            name='Fetch space data and send notifications',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Scheduler started successfully.")
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
