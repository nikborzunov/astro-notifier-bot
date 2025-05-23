# app/telegram_bot/ui/message.py

from app.telegram_bot.ui.keyboard import create_keyboard
from app.utils.logger import logger


async def send_message_with_keyboard(query, message, parse_mode='HTML', is_subscription_active: bool = False):
    try:
        if hasattr(query, 'edit_message_text'):
            await query.edit_message_text(message, parse_mode=parse_mode)
            await query.edit_message_reply_markup(reply_markup=create_keyboard(is_subscription_active))
        elif hasattr(query, 'reply_text'):
            await query.reply_text(message, parse_mode=parse_mode, reply_markup=create_keyboard(is_subscription_active))
        else:
            logger.error(f"Invalid query object: {query}")
            error_message = "⚠️ Oops, something went wrong while sending the message. Please try again."
            if hasattr(query, 'edit_message_text'):
                await query.edit_message_text(error_message)
            else:
                await query.reply_text(error_message)
    except Exception as e:
        logger.error(f"Error while sending message with keyboard: {e}")
        error_message = "⚠️ Oops, something went wrong while sending the message. Please try again."
        if hasattr(query, 'edit_message_text'):
            await query.edit_message_text(error_message)
        else:
            await query.reply_text(error_message)
