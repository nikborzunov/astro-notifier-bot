# app/telegram_bot/handlers/commands/scheduler.py

from telegram import Update
from telegram.ext import ContextTypes

from app.core.scheduler import (
    is_scheduler_running,
    start_scheduler,
    stop_scheduler,
)
from app.telegram_bot.ui.keyboard import back_keyboard
from app.utils.logger import logger


async def scheduler_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, user_timezone: str):
    chat_id = str(update.effective_chat.id)

    if is_scheduler_running(chat_id):
        msg = "🌙 You are already subscribed to updates."
    else:
        await start_scheduler(context.application, chat_id, user_timezone)
        msg = "🚀 Subscribed! Cosmic updates are now on the way!"

    await update.callback_query.message.edit_text(msg, reply_markup=back_keyboard())


async def scheduler_stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)

    if not is_scheduler_running(chat_id):
        msg = "❌ You are not subscribed to updates."
    else:
        await stop_scheduler(chat_id)
        msg = "🛸 Unsubscribed from cosmic updates."

    await update.callback_query.message.edit_text(msg, reply_markup=back_keyboard())
