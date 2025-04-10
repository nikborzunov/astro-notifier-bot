# bot/handlers/neo_history.py

from datetime import datetime, timedelta
from services.nasa_api import get_near_earth_objects
from bot.handlers.utils.message_utils import send_message_with_keyboard
from data.database import insert_neo
from utils.logger import logger
from utils.neo_utils import build_neo_message

async def send_neo_history(update, context):
    try:
        today = datetime.utcnow().date()
        seven_days_ago = today - timedelta(days=7)

        neo_data = await get_near_earth_objects(start_date=seven_days_ago.isoformat(), end_date=today.isoformat())

        if neo_data:
            sorted_neo_data = sorted(
                neo_data,
                key=lambda x: x["estimated_diameter"]["meters"]["estimated_diameter_max"],
                reverse=True
            )
            top_3_neo = sorted_neo_data[:3]

            neo_message = build_neo_message(top_3_neo)
            await send_message_with_keyboard(update.message, neo_message)
        else:
            await send_message_with_keyboard(update.message, "⚠️ No Near-Earth Object events found for the last 7 days.")

    except Exception as e:
        logger.error(f"Error in sending NEO history data: {e}")
        await send_message_with_keyboard(update.message, "⚡ Something went wrong while fetching the NEO history! Please try again later.")
