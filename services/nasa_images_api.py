# services/nasa_images_api.py

import aiohttp
from datetime import datetime
import asyncio
from utils.logger import logger

NASA_IMAGES_API_BASE_URL = "https://images-api.nasa.gov"

async def get_nasa_images_by_date(date: str):
    try:
        year, month = datetime.strptime(date, "%Y-%m-%d").year, datetime.strptime(date, "%Y-%m-%d").month
        params = {"media_type": "image", "year_start": str(year), "year_end": str(year), "page": 1}
        headers = {"User-Agent": "astro-notifier/1.0"}

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{NASA_IMAGES_API_BASE_URL}/search", params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                resp.raise_for_status()
                items = (await resp.json()).get("collection", {}).get("items", [])

        if not items:
            return {"error": "No results found for this year."}

        matches = [
            {
                "title": data.get("title"),
                "description": data.get("description"),
                "nasa_id": data.get("nasa_id"),
                "date_created": data.get("date_created"),
                "preview_url": next((l.get("href") for l in item.get("links", []) if l.get("rel") == "preview"), None),
                "keywords": data.get("keywords", []),
                "center": data.get("center"),
                "photographer": data.get("photographer", "Unknown")
            }
            for item in items if (data := item.get("data", [None])[0])
            if (created := data.get("date_created")) and datetime.strptime(created[:10], "%Y-%m-%d").month == month
        ]

        return {"matches": matches} if matches else {"error": "No exact match found for the selected year and month.", "closest": items[:3]}

    except asyncio.TimeoutError:
        return {"error": "Request timed out. Please try again later."}
    except aiohttp.ClientError as e:
        return {"error": f"HTTP Error: {e}"}
    except Exception as e:
        return {"error": str(e)}