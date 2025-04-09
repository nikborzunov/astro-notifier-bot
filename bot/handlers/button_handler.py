# bot/handlers/button_handler.py

from bot.handlers.apod import send_apod
from bot.handlers.neo import send_neo
from bot.handlers.keyboard_utils import create_keyboard
from telegram import Update
from telegram.ext import CallbackContext
from utils.logger import logger

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    loading_message = "Loading... 🚀"
    await query.edit_message_text(loading_message)

    if query.data == 'apod':
        await send_apod(query)
    elif query.data == 'neo':
        await send_neo(query)
