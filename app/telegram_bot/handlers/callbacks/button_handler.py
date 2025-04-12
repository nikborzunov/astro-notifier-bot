# app/telegram_bot/handlers/callbacks/button_handler.py

from telegram import Update
from telegram.ext import CallbackContext
from app.telegram_bot.handlers.commands.apod import send_apod, ask_for_apod_date
from app.telegram_bot.handlers.commands.neo import send_neo
from app.telegram_bot.handlers.commands.neo_history import send_neo_history
from app.telegram_bot.handlers.commands.scheduler import scheduler_start_command, scheduler_stop_command
from app.telegram_bot.ui.message import send_message_with_keyboard
from app.core.scheduler import is_scheduler_running
from app.utils.logger import logger

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    loading_message = await query.message.reply_text("⏳ Please wait...")

    try:
        content_message = None

        if query.data == "apod":
            content_message = await send_apod(update)
        elif query.data == "neo":
            content_message = await send_neo(update, query)
        elif query.data == "neo_history":
            content_message = await send_neo_history(update, query, context)
        elif query.data == "apod_by_date":
            await loading_message.delete()
            await ask_for_apod_date(update, context)
            return
        elif query.data == "start_scheduler":
            user_timezone = "Europe/Moscow"
            content_message = await scheduler_start_command(update, context, user_timezone)
        elif query.data == "stop_scheduler":
            content_message = await scheduler_stop_command(update, context)
        elif query.data == "menu":
            content_message = (
                "👋 <b>Welcome back to the main menu!</b>\n\n"
                "Select one of the options below to explore the universe 🌌"
            )
        else:
            logger.warning(f"⚠️ Unrecognized button callback: {query.data}")
            content_message = "❓ Unknown action. Please try another button."

        await loading_message.delete()

        chat_id = update.effective_user.id
        is_subscription_active = is_scheduler_running(chat_id)
        if content_message:
            await send_message_with_keyboard(query.message, content_message, parse_mode="HTML", is_subscription_active=is_subscription_active)

    except Exception as e:
        logger.error(f"💥 Error during button handling: {e}")
        await loading_message.delete()
        chat_id = update.effective_user.id
        is_subscription_active = is_scheduler_running(chat_id)
        await send_message_with_keyboard(query.message, "⚠️ Something went wrong. Please try again later.", is_subscription_active=is_subscription_active)
