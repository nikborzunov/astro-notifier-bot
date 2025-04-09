# bot/handlers/apod.py

from services.nasa_api import get_apod
from bot.handlers.message_utils import send_message_with_keyboard
from utils.logger import logger

async def send_apod(query):
    try:
        apod_data = get_apod()
        if apod_data:
            apod_title = apod_data["title"]
            apod_url = apod_data["url"]
            apod_date = apod_data["date"]

            # Form the detailed message with description and link
            apod_message = (
                f"🌌 **Astronomy Picture of the Day** 🌠\n\n"
                f"**Title**: {apod_title}\n"
                f"**Date**: {apod_date}\n\n"
                f"Here is the Astronomy Picture of the Day! It is carefully chosen to highlight a fascinating object or phenomenon in the sky.\n\n"
                f"🖼️ [View the full image here]({apod_url})\n\n"
                f"Enjoy and keep looking up! 🌟"
            )
        else:
            apod_message = "Sorry, I couldn't fetch the Astronomy Picture of the Day right now."

        # Send the message with keyboard
        await send_message_with_keyboard(query, apod_message)
        logger.info(f"Sent APOD data to {query.from_user.username}")
    except Exception as e:
        logger.error(f"Error in APOD: {e}")
        await send_message_with_keyboard(query, "Oops, something went wrong while fetching the APOD!")
