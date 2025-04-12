# app/telegram_bot/bot.py

import os
from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from app.core.scheduler import is_scheduler_running
from app.telegram_bot.handlers.callbacks.button_handler import button
from app.telegram_bot.handlers.commands.apod import handle_user_apod_date
from app.telegram_bot.handlers.commands.scheduler import (
    scheduler_start_command,
    scheduler_stop_command,
)
from app.telegram_bot.handlers.commands.start import start
from app.utils.logger import logger


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

def setup_bot(application: Application):
    try:
        def start_with_subscription(update, context):
            chat_id = update.effective_user.id
            is_subscription_active = is_scheduler_running(chat_id)
            return start(update, is_subscription_active)

        application.add_handler(CommandHandler("start", start_with_subscription))
        application.add_handler(CallbackQueryHandler(button))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_apod_date))
        application.add_handler(CommandHandler("scheduler_start", scheduler_start_command))
        application.add_handler(CommandHandler("scheduler_stop", scheduler_stop_command))

    except Exception as e:
        logger.error(f"❌ Error during bot setup: {e}")
        raise


def start_bot():
    setup_bot(application)
    application.run_polling(drop_pending_updates=True)
