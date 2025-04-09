import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    try:
        user = update.effective_user
        logger.info(f"User {user.username} started the bot.")
        
        # Send welcome message
        await update.message.reply_text("Welcome to AstroNotifierBot! Stay tuned for space updates.")
        logger.info(f"Sent welcome message to {user.username}")
    except Exception as e:
        logger.error(f"Error in /start command: {e}")
        await update.message.reply_text("Oops, something went wrong! Please try again later.")
        logger.error(f"Error response sent to {update.effective_user.username}")

# Initialize the application and add handlers
def main():
    try:
        # Create Application with the token
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        logger.info("Application created successfully")
    except Exception as e:
        logger.error(f"Error creating application: {e}")
        return

    # Add handler for /start command
    application.add_handler(CommandHandler("start", start))

    try:
        # Start the bot
        logger.info("Bot is starting...")
        application.run_polling()  # Use run_polling without event loop
    except Exception as e:
        logger.error(f"Error while running the bot: {e}")

if __name__ == '__main__':
    main()
