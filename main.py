# main.py

from app.db.database import create_tables
from app.telegram_bot.bot import start_bot


if __name__ == '__main__':
    create_tables()
    start_bot()
