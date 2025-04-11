# bot/handlers/keyboard_utils.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_keyboard():
    keyboard = [
        [InlineKeyboardButton("Astronomy Picture of the Day", callback_data="apod")],
        [InlineKeyboardButton("Latest 10 Near-Earth Objects", callback_data="neo")],
        [InlineKeyboardButton("Top 3 Potentially Hazardous NEOs in Last 7 Days", callback_data="neo_history")],
        [InlineKeyboardButton("APOD by Date", callback_data="apod_by_date")],
        [InlineKeyboardButton("🚀 Start Scheduler", callback_data="start_scheduler")],
        [InlineKeyboardButton("🛑 Stop Scheduler", callback_data="stop_scheduler")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_menu_button():
    return InlineKeyboardButton("⬅️ Back to Menu", callback_data="start")

def back_keyboard():
    return InlineKeyboardMarkup([[back_to_menu_button()]])
