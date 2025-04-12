# app/telegram_bot/handlers/commands/scheduler.py

from telegram import Update
from telegram.ext import ContextTypes
from app.telegram_bot.ui.keyboard import back_keyboard
from app.utils.logger import logger
from app.core.scheduler import start_scheduler, stop_scheduler, is_scheduler_running

async def scheduler_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)

    if is_scheduler_running(chat_id):
        msg = "⚠️ You already subscribed."
        logger.warning(f"chat_id {chat_id} tried to start scheduler but it's already running.")
    else:
        await start_scheduler(context.application, chat_id)
        msg = "✅ Scheduler started."

    await update.callback_query.message.edit_text(msg, reply_markup=back_keyboard())

async def scheduler_stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)

    if not is_scheduler_running(chat_id):
        msg = "⚠️ You already unsubscribed."
        logger.warning(f"chat_id {chat_id} tried to stop scheduler but it wasn't running.")
    else:
        await stop_scheduler(chat_id)
        msg = "🛑 Scheduler stopped."

    await update.callback_query.message.edit_text(msg, reply_markup=back_keyboard())
