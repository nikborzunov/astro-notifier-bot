# bot/handlers/start.py

from telegram import Update
from telegram.ext import CallbackContext
from bot.handlers.keyboard_utils import create_keyboard
from utils.logger import logger

# Function to handle /start command
async def start(update: Update, context: CallbackContext):
    try:
        user = update.effective_user
        logger.info(f"User {user.username} started the bot.")
        
        # Description of the bot
        bot_description = (
            "Welcome to AstroNotifierBot! 🌌\n\n"
            "This bot provides you with information about:\n"
            "- Astronomy Picture of the Day 🌠\n"
            "- Near-Earth Objects (asteroids) 🚀\n\n"
            "Choose an option below to get started!"
        )
        
        # Send welcome message with bot description and inline keyboard (buttons below input field)
        await update.message.reply_text(bot_description, reply_markup=create_keyboard())
        logger.info(f"Sent welcome message to {user.username}")
    except Exception as e:
        logger.error(f"Error in /start command: {e}")
        await update.message.reply_text("Oops, something went wrong! Please try again later.")
