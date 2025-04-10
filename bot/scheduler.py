# bot/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from services.nasa_api import get_apod
from data.database import insert_apod
from services.notifications import send_notification
from services.neo_alert_service import fetch_and_notify_neo

logger = logging.getLogger(__name__)

async def scheduled_task():
    try:
        apod_data = await get_apod()
        if apod_data:
            title = apod_data["title"]
            url = apod_data["url"]
            date = apod_data["date"]
            insert_apod(title, url, date)
            send_notification(f"Today's APOD: {title} - {url}")

        await fetch_and_notify_neo()

    except Exception as e:
        logger.error(f"Error in scheduled task: {e}")

def start_scheduler():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            scheduled_task,
            IntervalTrigger(seconds=3600),
            id='space_data_task',
            name='Fetch space data and send notifications',
            replace_existing=True
        )
        scheduler.start()
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
