# bot/handlers/message_utils.py

from bot.handlers.keyboard_utils import create_keyboard  # Import create_keyboard
from utils.logger import logger

async def send_message_with_keyboard(query, message):
    try:
        await query.edit_message_text(message)
        await query.edit_message_reply_markup(reply_markup=create_keyboard())
    except Exception as e:
        logger.error(f"Error while sending message with keyboard: {e}")
        await query.edit_message_text("Oops, something went wrong while sending the message.")
