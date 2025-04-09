from utils.logger import logger  # Import logger from utils.logger

# Function to send notifications
def send_notification(message: str):
    try:
        # Logic for sending notifications
        logger.info(f"Sending notification: {message}")
        # Here you should add the actual logic to send notifications (Telegram, email, etc.)
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
