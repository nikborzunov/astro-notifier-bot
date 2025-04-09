# bot/handlers/keyboard_utils.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Astronomy Picture of the Day", callback_data='apod')],
        [InlineKeyboardButton("Near-Earth Objects", callback_data='neo')]
    ])
