# main.py

from bot.telegram_bot import start_bot
from data.database import create_tables

if __name__ == '__main__':
    create_tables()
    start_bot()
