# app/services/nasa_data.py

import asyncio
import os
import aiohttp
from dotenv import load_dotenv

from app.utils.logger import logger

from .nasa_images import get_nasa_images_by_date


load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_BASE_URL = "https://api.nasa.gov/"

async def fetch_data(url, params=None, retries=3):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                resp.raise_for_status()
                return await resp.json()
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        if retries > 0:
            logger.warning(f"Retrying due to error: {e}")
            return await fetch_data(url, params, retries - 1)
        logger.error(f"Request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

async def get_apod():
    return await fetch_data(f"{NASA_BASE_URL}planetary/apod", {"api_key": NASA_API_KEY})

async def get_near_earth_objects(start_date=None, end_date=None):
    try:
        if not start_date or not end_date:
            from datetime import datetime
            today = datetime.utcnow().date().isoformat()
            start_date = today
            end_date = today
        
        url = f"{NASA_BASE_URL}neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={NASA_API_KEY}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

                if "near_earth_objects" in data:
                    neo_dict = data["near_earth_objects"]
                    neo_list = []
                    for date_neos in neo_dict.values():
                        neo_list.extend(date_neos)
                    return neo_list
                else:
                    print("Error: 'near_earth_objects' not found in the response.")
                    return None
    except Exception as e:
        print(f"Error fetching Near-Earth Objects: {e}")
        return None

async def get_apod_by_date(date: str):
    try:
        images = await get_nasa_images_by_date(date)
        if 'error' in images:
            return {
                "error": images['error'],
                "all_photos": [
                    {
                        "title": img.get("title", "No title"),
                        "description": img.get("description", "No description"),
                        "date_created": img.get("date_created", date),
                        "image_url": img.get("preview_url", ""),
                        "nasa_id": img.get("nasa_id", "")
                    } for img in images.get("closest", [])
                ]
            }

        exact = images.get("matches", [])
        formatted = [
            {
                "title": img.get("title", "No title"),
                "description": img.get("description", "No description"),
                "date_created": img.get("date_created", date),
                "image_url": img.get("preview_url", ""),
                "nasa_id": img.get("nasa_id", "")
            } for img in exact
        ]

        return {"exact_matches": formatted, "all_photos": formatted} if formatted else {"error": "No matches found."}
    except Exception as e:
        logger.error(f"Error fetching APOD by date: {e}")
        return {"error": "An error occurred while fetching the data."}