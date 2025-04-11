# app/telegram_bot/ui/menu.py

from telegram import Update
from telegram.ext import ContextTypes
from app.telegram_bot.ui.keyboard import create_keyboard

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.edit_text(
        "🌌 *Welcome to the Space Bot Menu!*",
        reply_markup=create_keyboard(),
        parse_mode="Markdown"
    )
