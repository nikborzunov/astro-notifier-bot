# app/telegram_bot/handlers/commands/neo.py

from app.services.nasa_data import get_near_earth_objects
from app.telegram_bot.ui.message import send_message_with_keyboard
from app.utils.logger import logger
from app.utils.neo_utils import build_neo_message
from datetime import datetime

async def send_neo(query):
    try:
        neo_data = await get_near_earth_objects()

        if neo_data:
            def get_approach_date(neo):
                try:
                    return datetime.strptime(neo["close_approach_data"][0]["close_approach_date"], "%Y-%m-%d")
                except:
                    return datetime.min

            sorted_neo = sorted(neo_data, key=get_approach_date, reverse=True)
            top_neo = sorted_neo[:10]

            neo_message = build_neo_message(top_neo)

            await send_message_with_keyboard(query, neo_message)
        else:
            await send_message_with_keyboard(query, "⚠️ No recent Near-Earth Object events found today.")
    
    except Exception as e:
        logger.error(f"Error in sending NEO data: {e}")
        await send_message_with_keyboard(query, "⚡ Something went wrong while fetching today's NEO data! Please try again later.")
