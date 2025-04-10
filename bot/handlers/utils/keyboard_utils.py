# bot/handlers/keyboard_utils.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_keyboard():
    keyboard = [
        [InlineKeyboardButton("Astronomy Picture of the Day", callback_data="apod")],
        [InlineKeyboardButton("Latest 10 Near-Earth Objects", callback_data="neo")],
        [InlineKeyboardButton("Top 3 Potentially Hazardous NEOs in Last 7 Days", callback_data="neo_history")],
        [InlineKeyboardButton("APOD by Date", callback_data="apod_by_date")]
    ]
    return InlineKeyboardMarkup(keyboard)
