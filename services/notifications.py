from utils.logger import logger

def send_notification(message: str):
    try:
        logger.info(f"Sending notification: {message}")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
