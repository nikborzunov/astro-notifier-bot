# app/services/notifications.py

from app.utils.logger import logger
from app.telegram_bot.ui.keyboard import back_keyboard, create_keyboard

async def send_notification(
    message: str, 
    chat_id: str, 
    application, 
    is_back_button_only: bool = False, 
    is_subscription_active: bool = False
):
    try:
        reply_markup = back_keyboard() if is_back_button_only else create_keyboard(is_subscription_active)

        await application.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

    except Exception as e:
        logger.error(f"Error sending notification to {chat_id}: {e}")
