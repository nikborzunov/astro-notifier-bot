# bot/handlers/button_handler.py

from bot.handlers.apod.apod import send_apod
from bot.handlers.neo.neo import send_neo
from bot.handlers.neo.neo_history import send_neo_history
from bot.handlers.apod.apod_by_date import ask_for_date
from bot.handlers.utils.keyboard_utils import create_keyboard
from bot.handlers.scheduler_commands import scheduler_start_command, scheduler_stop_command
from telegram import Update
from telegram.ext import CallbackContext
from utils.logger import logger

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    loading_message = await query.message.reply_text("⏳ Please wait...")

    try:
        content_message = None

        if query.data == "apod":
            content_message = await send_apod(query)
        elif query.data == "neo":
            content_message = await send_neo(query)
        elif query.data == "neo_history":
            content_message = await send_neo_history(query, context)
        elif query.data == "apod_by_date":
            await loading_message.delete()
            await ask_for_date(update, context)
            return
        elif query.data == "start_scheduler":
            content_message = await scheduler_start_command(update, context)
        elif query.data == "stop_scheduler":
            content_message = await scheduler_stop_command(update, context)
        else:
            logger.warning(f"⚠️ Unrecognized button callback: {query.data}")
            content_message = "❓ Unknown action. Please try another button."

        await loading_message.delete()

        if content_message:
            await query.message.reply_text(content_message, reply_markup=create_keyboard())

    except Exception as e:
        logger.error(f"💥 Error during button handling: {e}")
        await loading_message.delete()
        await query.message.reply_text("⚠️ Something went wrong. Please try again later.", reply_markup=create_keyboard())
