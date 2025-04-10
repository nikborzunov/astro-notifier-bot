# services/nasa_images_api.py

import aiohttp
from datetime import datetime
import asyncio
from utils.logger import logger

NASA_IMAGES_API_BASE_URL = "https://images-api.nasa.gov"

SPACE_KEYWORDS = [
    "space", "planet", "galaxy", "universe", "nebula", "black hole", "asteroid", "star", 
    "cosmos", "astronomy", "exoplanet", "satellite", "orbit", "milky way", "spacecraft", 
    "rocket", "astronaut", "moon", "comet", "supernova", "constellation", "cluster", 
    "eclipse", "exoplanets", "celestial", "solar system", "space exploration", "mars", 
    "jupiter", "saturn", "venus", "earth", "telescope", "star cluster", "quasar", 
    "interstellar", "orbiting", "astronomical", "light year", "space station", "NASA", 
    "Hubble", "pulsar", "event horizon", "black hole", "space mission", "lunar", 
    "milkyway", "planetary", "voyager", "stardust", "solar flare", "dark matter", 
    "light pollution", "space weather", "asteroid belt", "solar wind", "space debris", 
    "space-time", "extragalactic", "gravitational waves", "solar eclipse", "gravitational lensing", 
    "quantum physics", "planetary nebula", "galactic center", "dark energy", "cosmic radiation", 
    "cosmic microwave background", "space dust", "radio galaxy", "gamma ray", "pulsar wind", 
    "solar corona", "stellar wind", "light curve", "supernova remnant", "astronomical observatory", 
    "solar maximum", "space exploration technology", "lunar surface", "solar system bodies", 
    "cosmic rays", "solar flare", "black hole merger", "stellar explosion", "tides in space", 
    "astrochemistry", "intergalactic medium", "cosmic inflation", "stellar evolution", "planetary rings", 
    "Hawking radiation", "radio astronomy", "space-based telescope", "planetary system", 
    "planetary atmosphere", "interstellar medium", "gravitational collapse", "heliospheric", 
    "space mission", "space-time anomalies", "space-time curvature", "supermassive black hole", 
    "orbital dynamics", "stellar spectra", "astrobiology", "stellar mass", "galactic dust", 
    "planetary migration", "solar wind pressure", "space-time continuum", "light pollution control", 
    "stellar core", "exoplanetary system", "cosmology", "orbital mechanics", "heliophysics", 
    "galactic evolution", "stardust", "orbital decay", "space probe", "space exploration rover", 
    "space mission planning", "astro-imaging", "extra-solar planets", "gravitational wave detection", 
    "space radiation", "space launch", "galactic evolution", "dark matter halo", "galactic merger", 
    "cosmic horizon", "black hole accretion", "exoplanet discovery", "multi-wavelength astronomy", 
    "space observatory", "stellar remnants", "gamma ray burst", "neutron star", "spacetime ripples", 
    "Lagrange point", "orbital research", "extragalactic astronomy", "magnetosphere", "stellar chemistry", 
    "dark matter detection", "cosmic inflation", "quantum gravity", "extra-terrestrial", "space station", 
    "galactic core", "spacetime anomalies"
]

async def get_nasa_images_by_date(date: str):
    try:
        year, month = datetime.strptime(date, "%Y-%m-%d").year, datetime.strptime(date, "%Y-%m-%d").month
        
        params = {
            "media_type": "image",
            "keywords": ",".join(SPACE_KEYWORDS),
            "year_start": str(year),
            "year_end": str(year),
            "page": 1,
            "page_size": 10
        }

        headers = {"User-Agent": "astro-notifier/1.0"}

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{NASA_IMAGES_API_BASE_URL}/search", params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                resp.raise_for_status()
                data = await resp.json()
                items = data.get("collection", {}).get("items", [])

        if not items:
            return {"error": "No results found for this year."}

        matches = [
            {
                "title": item.get("data", [{}])[0].get("title"),
                "description": item.get("data", [{}])[0].get("description"),
                "nasa_id": item.get("data", [{}])[0].get("nasa_id"),
                "date_created": item.get("data", [{}])[0].get("date_created"),
                "preview_url": next((link.get("href") for link in item.get("links", []) if link.get("rel") == "preview"), None),
                "keywords": item.get("data", [{}])[0].get("keywords", []),
                "center": item.get("data", [{}])[0].get("center"),
                "photographer": item.get("data", [{}])[0].get("photographer", "Unknown")
            }
            for item in items if item.get("data")
        ]

        return {"matches": matches} if matches else {"error": "No exact match found for the selected year and month."}

    except asyncio.TimeoutError:
        return {"error": "Request timed out. Please try again later."}
    except aiohttp.ClientError as e:
        return {"error": f"HTTP Error: {e}"}
    except Exception as e:
        return {"error": str(e)}