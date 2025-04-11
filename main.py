# main.py

from app.telegram_bot.bot import start_bot
from app.db.database import create_tables

if __name__ == '__main__':
    create_tables()
    start_bot()
