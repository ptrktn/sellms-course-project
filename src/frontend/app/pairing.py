import requests
import ollama
import os

from config import OLLAMA_HOST, OLLAMA_MODEL, DEFAULT_REGION, DEFAULT_HEMISPHERE
from datetime import datetime

os.environ['OLLAMA_HOST'] = OLLAMA_HOST

def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return "ISO 3166-1 country code " + data.get("country", "unknown")
    except Exception as e:
        print(f"Error fetching location: {e}")
        return "unknown"

def get_country_and_season():
    month = int(datetime.utcnow().month)
    # Get IP info
    try:
        ipinfo = requests.get("https://ipinfo.io/json").json()
        loc = ipinfo.get("loc", "0,0")
        lat = float(loc.split(",")[0]) if "," in loc else 0.0
        country = ipinfo.get("country", "unknown")
        # Determine hemisphere
        hemisphere = "northern" if lat >= 0 else "southern"
    except Exception as e:
        print(f"Error fetching IP info: {e}")
        country = DEFAULT_REGION
        hemisphere = DEFAULT_HEMISPHERE
    
    # Assign seasons based on hemisphere
    if hemisphere == "northern":
        if month in [12, 1, 2]:
            season = "winter"
        elif month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        else:
            season = "autumn"
    else:
        if month in [12, 1, 2]:
            season = "summer"
        elif month in [3, 4, 5]:
            season = "autumn"
        elif month in [6, 7, 8]:
            season = "winter"
        else:
            season = "spring"
    return f"ISO 3166-1 country code {country}", season

def generate_pairing(season, location, preferences):
    if not season and not location:
        location, season = get_country_and_season()
    else:
        location = location if location else get_location()
        if not season or (season.lower() not in ["spring", "summer", "autumn", "winter"]):
            _, season = get_country_and_season()

    prompt = f"""
        Suggest a wine cheese pairing based on the following criteria:\n
        
        - The season is {season}\n
        - The location is {location}\n\n

        Answer briefly in a single paragraph in plain text without any markup formatting.\n
        Include a brief rationale for the pairing, touching on style, region, and seasonal cues.\n
        Include serving notes if relevant.\n
        If you cannot determine a good pairing, say so.\n
        """

    response = ollama.generate(
        model = OLLAMA_MODEL,
        prompt = prompt
    )
    data = {
        "response": response['response']
    }

    return data
