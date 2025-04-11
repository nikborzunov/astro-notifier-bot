# app/core/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from app.services.nasa_data import get_apod
from app.db.database import insert_apod
from app.services.notifications import send_notification
from app.services.neo_notifier import fetch_and_notify_neo

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def is_scheduler_running():
    return scheduler.running

async def scheduled_task():
    try:
        apod_data = await get_apod()
        if apod_data:
            title = apod_data["title"]
            url = apod_data["url"]
            date = apod_data["date"]
            insert_apod(title, url, date)
            send_notification(f"🖼️ Today's APOD: {title} - {url}")
        await fetch_and_notify_neo()
    except Exception as e:
        logger.error(f"❌ Error in scheduled task: {e}")

async def start_scheduler():
    if scheduler.running:
        logger.warning("⚠️ Scheduler is already running.")
        return
    scheduler.add_job(
        scheduled_task,
        trigger=IntervalTrigger(hours=1),
        id='space_data_task',
        name='Fetch space data and send notifications',
        replace_existing=True
    )
    scheduler.start()

async def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
    else:
        logger.warning("⚠️ Scheduler is not running.")
