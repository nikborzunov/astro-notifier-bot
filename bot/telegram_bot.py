import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.handlers.start import start  # Import the start function
from bot.handlers.button_handler import button  # Import the button handler
from bot.scheduler import start_scheduler  # Import the scheduler start function
from utils.logger import logger  # Import the logger from utils

# Load environment variables from the .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Function to create and start the bot
def start_bot():
    try:
        # Start the scheduler before launching the bot
        start_scheduler()
        
        # Create the Application with the bot token
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        logger.info("Application created successfully")
        
        # Add handlers for /start command and button presses
        application.add_handler(CommandHandler("start", start))  # /start command
        application.add_handler(CallbackQueryHandler(button))  # Button press handler
        
        logger.info("Bot is starting...")
        application.run_polling(drop_pending_updates=True)  # Start the bot with the flag to drop duplicate updates
    except Exception as e:
        logger.error(f"Error while running the bot: {e}")
