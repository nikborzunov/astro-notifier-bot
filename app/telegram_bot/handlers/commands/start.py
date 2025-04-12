# app/telegram_bot/handlers/commands/start.py

from telegram import Update

from app.telegram_bot.ui.keyboard import create_keyboard
from app.utils.logger import logger

async def start(update: Update, is_subscription_active: bool = False):
    try:
        user = update.effective_user

        bot_description = (
            "*🌌 Welcome to AstroNotifierBot!* 🚀\n\n"
            "This bot brings the wonders of space to your fingertips! 🌠 Explore the universe with just a few taps.\n\n"
            "*Features:* ⭐\n"
            "1️⃣ *Astronomy Picture of the Day* – Stunning images from space to amaze you every day.\n"
            "2️⃣ *Near-Earth Objects (asteroids)* – Stay updated on the latest asteroid data that might pass near Earth! 🚀\n"
            "3️⃣ *NEO History (Last 7 Days)* – Discover the recent history of near-Earth objects and space events 🌍\n\n"
            "👉 Choose an option below to start your space adventure! ✨"
        )

        await update.message.reply_text(bot_description, reply_markup=create_keyboard(is_subscription_active), parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error in /start command for user {user.username} ({user.id}): {e}")
        await update.message.reply_text("⚠️ Oops, something went wrong! Please try again later. 💥")
