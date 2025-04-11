# app/telegram_bot/bot.py

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from app.telegram_bot.handlers.commands.start import start
from app.telegram_bot.handlers.callbacks.button_handler import button
from app.telegram_bot.handlers.commands.apod import handle_user_apod_date
from app.telegram_bot.handlers.commands.scheduler import scheduler_start_command, scheduler_stop_command
from app.utils.logger import logger
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start_bot():
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_apod_date))
        application.add_handler(CommandHandler("scheduler_start", scheduler_start_command))
        application.add_handler(CommandHandler("scheduler_stop", scheduler_stop_command))

        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"❌ Error while running the bot: {e}")
