# bot/handlers/apod_by_date.py

from telegram import Update
from bot.handlers.utils.message_utils import send_message_with_keyboard
from utils.logger import logger
from datetime import datetime
from services.nasa_api import get_apod_by_date

async def ask_for_date(update, context):
    try:
        query = update.callback_query
        if not query or not query.message:
            logger.error("Missing callback_query or message")
            return

        await send_message_with_keyboard(
            query.message,
            "📅 *Please enter a date* for APOD (in the format `YYYY-MM-DD`).\nExample: `1996-09-07` or `2020-01-01`."
        )
        context.user_data['waiting_for_date'] = True
        logger.info(f"Waiting for date input from user {query.from_user.username}")
    except Exception as e:
        logger.error(f"ask_for_date error: {e}")
        if update.callback_query and update.callback_query.message:
            await update.callback_query.message.reply_text("⚠️ Something went wrong. Please try again later.")

async def handle_user_date(update, context):
    if not context.user_data.get('waiting_for_date'):
        return

    user_input = update.message.text.strip()
    try:
        selected_date = datetime.strptime(user_input, "%Y-%m-%d").date()
        context.user_data['waiting_for_date'] = False

        query = update.callback_query if update.callback_query else None
        message = update.message if update.message else None

        loading_message = f"✅ *Date received:* {selected_date}. Searching for the image... ⏳"
        loading_message_sent = await (query.message if query else message).reply_text(loading_message)

        apod_data = await get_apod_by_date(selected_date.strftime('%Y-%m-%d'))
        if 'error' in apod_data:
            await send_message_with_keyboard(message or query.message, f"⚠️ *Error:* {apod_data['error']}")
            await loading_message_sent.delete()
            return

        image = apod_data.get("all_photos", [])[0] if apod_data.get("all_photos") else None
        if not image:
            await send_message_with_keyboard(
                message or query.message,
                f"⚠️ *No images found* for *{selected_date}*. Try a different date."
            )
            await loading_message_sent.delete()
            return

        actual_date = datetime.strptime(image.get("date_created", str(selected_date))[:10], "%Y-%m-%d").date()
        prefix = (
            f"🌟 *Exact match found* for {actual_date}!"
            if actual_date == selected_date
            else f"🔎 *No image for {selected_date}. Showing the closest one from* *{actual_date}*."
        )

        msg = (
            f"🔎 *No image found for* {selected_date}.\n"
            f"👉 *Showing the closest image from* *{actual_date}*:\n\n"
            f"✨ *{image.get('title', 'No Title')}* ✨\n\n"
            f"📖 *Description*: {image.get('description', 'No Description available')}\n\n"
            f"🔗 *[View Image]({image.get('image_url', '')})*\n\n"
            f"🆔 *NASA ID*: `{image.get('nasa_id', '')}`\n\n"
            f"🌐 Explore more images and details on [NASA's platform](https://images.nasa.gov/)"
        )
        
        await send_message_with_keyboard(message or query.message, msg)
        await loading_message_sent.delete()

    except ValueError:
        await send_message_with_keyboard(message or query.message, "⚠️ *Invalid date format*. Please use `YYYY-MM-DD`. For example, `2020-12-15`.")
    except Exception as e:
        logger.error(f"handle_user_date error: {e}")
        await send_message_with_keyboard(message or query.message, "⚠️ *Error processing your request*. Please try again later.")
