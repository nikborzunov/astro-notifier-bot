# app/telegram_bot/handlers/commands/scheduler.py

from telegram import Update
from telegram.ext import ContextTypes
from app.core.scheduler import start_scheduler, stop_scheduler, is_scheduler_running
from app.telegram_bot.ui.keyboard import back_keyboard

async def scheduler_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_scheduler_running():
        msg = "⚠️ Scheduler is already running."
        await update.callback_query.message.edit_text(msg, reply_markup=back_keyboard())
    else:
        await start_scheduler()
        msg = "✅ Scheduler started."
        await update.callback_query.message.edit_text(msg, reply_markup=back_keyboard())

async def scheduler_stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_scheduler_running():
        msg = "⚠️ Scheduler is not running."
    else:
        await stop_scheduler()
        msg = "🛑 Scheduler stopped."
    await update.callback_query.message.edit_text(msg, reply_markup=back_keyboard())
