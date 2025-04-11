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
            "📅 <b>Please enter a date</b> for APOD (in the format <code>YYYY-MM-DD</code>). Example: <code>1996-09-07</code> or <code>2020-01-01</code>."
        )
        context.user_data['waiting_for_date'] = True
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

        loading_message = f"✅ <b>Date received:</b> {selected_date}. Searching for the image... ⏳"
        loading_message_sent = await (query.message if query else message).reply_text(loading_message, parse_mode='HTML')

        apod_data = await get_apod_by_date(selected_date.strftime('%Y-%m-%d'))
        if 'error' in apod_data:
            await send_message_with_keyboard(message or query.message, f"⚠️ <b>Error:</b> {apod_data['error']}", parse_mode='HTML')
            await loading_message_sent.delete()
            return

        image = apod_data.get("all_photos", [])[0] if apod_data.get("all_photos") else None
        if not image:
            await send_message_with_keyboard(
                message or query.message,
                f"⚠️ <b>No images found</b> for <b>{selected_date}</b>. Try a different date.",
                parse_mode='HTML'
            )
            await loading_message_sent.delete()
            return

        actual_date = datetime.strptime(image.get("date_created", str(selected_date))[:10], "%Y-%m-%d").date()
        prefix = (
            f"🌟 <b>Exact match found</b> for {actual_date}!"
            if actual_date == selected_date
            else f"🔎 <b>No image for {selected_date}. Showing the closest one from</b> <b>{actual_date}</b>."
        )

        msg = (
            f"🔎 <b>No image found for</b> {selected_date}.\n"
            f"👉 <b>Showing the closest image from</b> <b>{actual_date}</b>:\n\n"
            f"✨ <b>{image.get('title', 'No Title')}</b> ✨\n\n"
            f"📖 <b>Description</b>: {image.get('description', 'No Description available')}\n\n"
            f"🔗 <b><a href='{image.get('image_url', '')}'>View Image</a></b>\n\n"
            f"🆔 <b>NASA ID</b>: <code>{image.get('nasa_id', '')}</code>\n\n"
            f"🌐 Explore more images and details on <a href='https://images.nasa.gov/'>NASA's platform</a>"
        )
        
        await send_message_with_keyboard(message or query.message, msg, parse_mode='HTML')

        await loading_message_sent.delete()

    except ValueError:
        await send_message_with_keyboard(message or query.message, "⚠️ <b>Invalid date format</b>. Please use <code>YYYY-MM-DD</code>. For example, <code>2020-12-15</code>.", parse_mode='HTML')
    except Exception as e:
        logger.error(f"handle_user_date error: {e}")
        await send_message_with_keyboard(message or query.message, "⚠️ <b>Error processing your request</b>. Please try again later.", parse_mode='HTML')
