# app/core/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.nasa_data import get_apod
from app.db.database import insert_apod, save_user_chat_id, unsubscribe_user, is_user_subscribed
from app.services.notifications import send_notification

scheduler = AsyncIOScheduler()

_app = None
user_jobs = {}

APOD_JOB_NAME = "Fetch APOD and send notification daily"
DEFAULT_INTERVAL_SECONDS = 86400

def is_scheduler_running(chat_id: str) -> bool:
    return bool(is_user_subscribed(chat_id))

def set_application_instance(application):
    global _app
    _app = application

async def create_apod_message(apod_data):
    title, url, date = apod_data["title"], apod_data["url"], apod_data["date"]
    description = apod_data.get("explanation", "No description available.")
    author = apod_data.get("copyright", "Unknown Author")
    object_type = apod_data.get("object_type", "Unknown")

    insert_apod(title, url, date)

    message = (
        f"🌅 <b>Good morning, space explorer!</b>\n\n"
        f"You're subscribed to the <b>Astronomy Picture of the Day</b> 🌌\n"
        f"Here's your daily dose of cosmic wonder:\n\n"
        f"🗓️ <b>Date</b>: {date}\n"
        f"📌 <b>Title</b>: {title}\n\n"
        f"📖 <b>Description</b>:\n{description}\n\n"
        f"✍️ <b>Author</b>: {author}\n"
        f"🌠 <b>Object Type</b>: {object_type}\n\n"
        f"🖼️ <a href='{url}'>View the full image here</a>\n\n"
        f"🚀 <i>Keep exploring the universe with us!</i>"
    )
    return message

async def scheduled_task(chat_id: str):
    try:
        apod_data = await get_apod()

        if not apod_data:
            return

        message = await create_apod_message(apod_data)

        if is_user_subscribed(chat_id):
            await send_notification(message, chat_id, _app, False, is_subscription_active=is_scheduler_running(chat_id))
    except Exception as e:
        pass

async def start_scheduler(application, chat_id: str):
    if is_scheduler_running(chat_id):
        return

    set_application_instance(application)
    
    save_user_chat_id(chat_id)

    job = scheduler.add_job(
        scheduled_task,
        trigger=IntervalTrigger(seconds=DEFAULT_INTERVAL_SECONDS),
        id=f'apod_task_{chat_id}',
        args=[chat_id],
        name=f'{APOD_JOB_NAME} for chat_id {chat_id}',
        replace_existing=True,
        max_instances=1
    )

    user_jobs[chat_id] = job

    if not scheduler.running:
        scheduler.start()

async def stop_scheduler(chat_id: str):
    if chat_id not in user_jobs:
        return

    job = user_jobs[chat_id]
    
    scheduler.remove_job(job.id)

    del user_jobs[chat_id]

    unsubscribe_user(chat_id)
