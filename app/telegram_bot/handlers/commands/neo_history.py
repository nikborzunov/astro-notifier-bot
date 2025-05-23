# app/telegram_bot/handlers/commands/neo_history.py

from datetime import datetime, timedelta

from app.core.scheduler import is_scheduler_running
from app.services.nasa_data import get_near_earth_objects
from app.telegram_bot.ui.message import send_message_with_keyboard
from app.utils.logger import logger
from app.utils.neo_utils import build_neo_message


async def send_neo_history(update, query, context):
    try:
        chat_id = update.effective_user.id
        is_subscription_active = is_scheduler_running(chat_id)
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
            await send_message_with_keyboard(query.message, neo_message, is_subscription_active=is_subscription_active)
        else:
            await send_message_with_keyboard(query.message, "⚠️ No Near-Earth Object events found for the last 7 days.", is_subscription_active=is_subscription_active)

    except Exception as e:
        logger.error(f"Error in sending NEO history data: {e}")
        await send_message_with_keyboard(query.message, "⚡ Something went wrong while fetching the NEO history! Please try again later.", is_subscription_active=is_subscription_active)

