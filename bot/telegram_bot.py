# bot/telegram_bot.py

import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.handlers.start import start
from bot.handlers.button_handler import button
from bot.handlers.apod.apod_by_date import handle_user_date
from bot.scheduler import start_scheduler
from utils.logger import logger

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start_bot():
    try:
        start_scheduler()
        
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))
        
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_date))
        
        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Error while running the bot: {e}")
