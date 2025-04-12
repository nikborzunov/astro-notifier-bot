# app/telegram_bot/ui/keyboard.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_keyboard(is_subscription_active: bool = False):
    keyboard = [
        [InlineKeyboardButton("🌌 Astronomy Pic of the Day", callback_data="apod")],
        [InlineKeyboardButton("☄️ Latest 10 NEOs", callback_data="neo")],
        [InlineKeyboardButton("🛸 Top 3 Hazardous NEOs", callback_data="neo_history")],
        [InlineKeyboardButton("📅 Pic by Date", callback_data="apod_by_date")],
    ]

    if is_subscription_active:
        keyboard.append([InlineKeyboardButton("🛑 Unsubscribe from Daily Pic", callback_data="stop_scheduler")])
    else:
        keyboard.append([InlineKeyboardButton("🚀 Subscribe for Daily Pic", callback_data="start_scheduler")])

    return InlineKeyboardMarkup(keyboard)

def back_to_menu_button():
    return InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu")

def back_keyboard():
    return InlineKeyboardMarkup([[back_to_menu_button()]])
