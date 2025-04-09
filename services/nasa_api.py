import requests
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")

# Base URL for NASA API
NASA_BASE_URL = "https://api.nasa.gov/"

# Function to get Astronomy Picture of the Day
def get_apod():
    try:
        url = f"{NASA_BASE_URL}planetary/apod?api_key={NASA_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching Astronomy Picture of the Day: {e}")
        return None

# Function to get Near-Earth Object data (asteroids)
def get_near_earth_objects(start_date=None, end_date=None):
    try:
        # Prepare the URL with the date range if provided
        if start_date and end_date:
            url = f"{NASA_BASE_URL}neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={NASA_API_KEY}"
        else:
            # Default URL for browsing NEOs if no dates provided
            url = f"{NASA_BASE_URL}neo/rest/v1/neo/browse?api_key={NASA_API_KEY}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors

        # Ensure the response is in JSON format
        try:
            data = response.json()
        except ValueError:
            print("Error: Response is not a valid JSON.")
            return None

        # Check if 'near_earth_objects' exists in the response
        if isinstance(data, dict) and "near_earth_objects" in data:
            return data["near_earth_objects"]
        else:
            print("Error: 'near_earth_objects' not found in the response.")
            return None
    except Exception as e:
        print(f"Error fetching Near-Earth Objects: {e}")
        return None
