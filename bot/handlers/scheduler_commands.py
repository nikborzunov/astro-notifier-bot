# bot/handlers/scheduler_commands.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.scheduler import start_scheduler, stop_scheduler, is_scheduler_running
from utils.logger import logger
from bot.handlers.utils.keyboard_utils import back_keyboard

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
