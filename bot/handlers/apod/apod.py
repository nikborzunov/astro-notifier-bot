# bot/handlers/apod.py

from services.nasa_api import get_apod
from bot.handlers.utils.message_utils import send_message_with_keyboard
from utils.logger import logger
from data.database import insert_apod

async def send_apod(query):
    try:
        apod_data = await get_apod()
        
        if apod_data:
            apod_title = apod_data["title"]
            apod_url = apod_data["url"]
            apod_date = apod_data["date"]
            apod_description = apod_data.get("explanation", "No description available.")
            apod_author = apod_data.get("copyright", "Unknown Author")
            apod_object_type = apod_data.get("object_type", "Unknown")
            
            apod_message = (
                f"🌌 <b>Astronomy Picture of the Day</b> 🌠\n\n"
                f"<b>Title</b>: {apod_title}\n"
                f"<b>Date</b>: {apod_date}\n\n"
                f"<b>Description</b>:\n{apod_description}\n\n"
                f"<b>Author</b>: {apod_author}\n"
                f"<b>Object Type</b>: {apod_object_type}\n\n"
                f"🌟 <b>Explore More!</b> 🌟\n"
                f"Here is the Astronomy Picture of the Day! It showcases a fascinating celestial object or phenomenon.\n\n"
                f"🖼️ <a href='{apod_url}'>View the full image here</a>\n\n"
                f"Keep looking up! ✨"
            )
            
            insert_apod(apod_title, apod_url, apod_date)

        else:
            apod_message = "⚠️ Sorry, I couldn't fetch the Astronomy Picture of the Day right now."

        await send_message_with_keyboard(query, apod_message)
    except Exception as e:
        logger.error(f"Error in APOD: {e}")  
        await send_message_with_keyboard(query, "⚡ Oops, something went wrong while fetching the APOD!")
