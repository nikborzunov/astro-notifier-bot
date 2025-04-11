# app/telegram_bot/handlers/commands/apod.py

from telegram import Update
from datetime import datetime
from app.services.nasa_data import get_apod, get_apod_by_date
from app.telegram_bot.ui.message import send_message_with_keyboard
from app.utils.logger import logger
from app.db.database import insert_apod

async def send_apod(update):
    try:
        apod_data = await get_apod()

        if apod_data:
            apod_title = apod_data["title"]
            apod_url = apod_data["url"]
            apod_date = apod_data["date"]
            apod_description = apod_data.get("explanation", "No description available.")
            apod_author = apod_data.get("copyright", "Unknown Author")
            apod_object_type = apod_data.get("object_type", "Unknown")

            apod_message = (
                f"🌌 <b>Astronomy Picture of the Day</b> 🌠\n\n"
                f"<b>Title</b>: {apod_title}\n"
                f"<b>Date</b>: {apod_date}\n\n"
                f"<b>Description</b>:\n{apod_description}\n\n"
                f"<b>Author</b>: {apod_author}\n"
                f"<b>Object Type</b>: {apod_object_type}\n\n"
                f"🌟 <b>Explore More!</b> 🌟\n"
                f"Here is the Astronomy Picture of the Day! It showcases a fascinating celestial object or phenomenon.\n\n"
                f"🖼️ <a href='{apod_url}'>View the full image here</a>\n\n"
                f"Keep looking up! ✨"
            )

            insert_apod(apod_title, apod_url, apod_date)
        else:
            apod_message = "⚠️ Sorry, I couldn't fetch the Astronomy Picture of the Day right now."

        await send_message_with_keyboard(update.callback_query.message, apod_message)
    except Exception as e:
        logger.error(f"Error in APOD: {e}")
        await send_message_with_keyboard(update.callback_query.message, "⚡ Oops, something went wrong while fetching the APOD!")

async def ask_for_apod_date(update, context):
    query = update.callback_query
    if not query or not query.message:
        logger.error("Missing callback_query or message")
        return

    await send_message_with_keyboard(
        query.message,
        "📅 <b>Please enter a date</b> for APOD (in the format <code>YYYY-MM-DD</code>). Example: <code>1996-09-07</code> or <code>2020-01-01</code>."
    )
    context.user_data['waiting_for_date'] = True

async def handle_user_apod_date(update, context):
    if not context.user_data.get('waiting_for_date'):
        return

    user_input = update.message.text.strip()
    try:
        selected_date = datetime.strptime(user_input, "%Y-%m-%d").date()
        context.user_data['waiting_for_date'] = False

        message = update.message

        loading_message = f"✅ <b>Date received:</b> {selected_date}. Searching for the image... ⏳"
        loading_message_sent = await message.reply_text(loading_message, parse_mode='HTML')

        apod_data = await get_apod_by_date(selected_date.strftime('%Y-%m-%d'))
        if 'error' in apod_data:
            await send_message_with_keyboard(message, f"⚠️ <b>Error:</b> {apod_data['error']}", parse_mode='HTML')
            await loading_message_sent.delete()
            return

        image = apod_data.get("all_photos", [])[0] if apod_data.get("all_photos") else None
        if not image:
            await send_message_with_keyboard(
                message,
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
            f"{prefix}\n\n"
            f"✨ <b>{image.get('title', 'No Title')}</b> ✨\n\n"
            f"📖 <b>Description</b>: {image.get('description', 'No Description available')}\n\n"
            f"🔗 <b><a href='{image.get('image_url', '')}'>View Image</a></b>\n\n"
            f"🆔 <b>NASA ID</b>: <code>{image.get('nasa_id', '')}</code>\n\n"
            f"🌐 Explore more images and details on <a href='https://images.nasa.gov/'>NASA's platform</a>"
        )

        await send_message_with_keyboard(message, msg, parse_mode='HTML')
        await loading_message_sent.delete()

    except ValueError:
        await send_message_with_keyboard(message, "⚠️ <b>Invalid date format</b>. Please use <code>YYYY-MM-DD</code>. For example, <code>2020-12-15</code>.", parse_mode='HTML')
    except Exception as e:
        logger.error(f"handle_user_apod_date error: {e}")
        await send_message_with_keyboard(message, "⚠️ <b>Error processing your request</b>. Please try again later.", parse_mode='HTML')
