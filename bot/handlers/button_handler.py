# bot/handlers/button_handler.py

from bot.handlers.apod import send_apod
from bot.handlers.neo import send_neo
from bot.handlers.neo_history import send_neo_history
from bot.handlers.keyboard_utils import create_keyboard
from telegram import Update
from telegram.ext import CallbackContext
from utils.logger import logger

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    loading_message = "⏳ Please wait... "
    loading_message_sent = await query.message.reply_text(loading_message)

    try:
        if query.data == 'apod':
            content_message = await send_apod(query)
        elif query.data == 'neo':
            content_message = await send_neo(query)
        elif query.data == 'neo_history':
            content_message = await send_neo_history(query, context)

        await loading_message_sent.delete()

        if not content_message:
            logger.error("Received empty content_message.")
            return

        await query.message.reply_text(content_message, reply_markup=create_keyboard())
    
    except Exception as e:
        logger.error(f"Error during button handling: {e}")
        await query.message.reply_text("⚠️ Something went wrong. Please try again later. 💥")
