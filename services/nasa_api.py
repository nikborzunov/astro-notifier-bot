import requests
import os
from dotenv import load_dotenv

load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")

NASA_BASE_URL = "https://api.nasa.gov/"

def get_apod():
    try:
        url = f"{NASA_BASE_URL}planetary/apod?api_key={NASA_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching Astronomy Picture of the Day: {e}")
        return None

def get_near_earth_objects(start_date=None, end_date=None):
    try:
        if not start_date or not end_date:
            from datetime import datetime
            today = datetime.utcnow().date().isoformat()
            start_date = today
            end_date = today
        
        url = f"{NASA_BASE_URL}neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={NASA_API_KEY}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

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
