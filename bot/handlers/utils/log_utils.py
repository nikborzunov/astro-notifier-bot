# bot/handlers/log_utils.py

from loguru import logger

def log_success(message: str):
    logger.success(f"✅ {message}")

def log_warning(message: str):
    logger.warning(f"⚠️ {message}")

def log_error(message: str):
    logger.error(f"❌ {message}")
