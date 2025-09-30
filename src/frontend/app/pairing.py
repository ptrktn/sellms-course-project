import requests
from config import OLLAMA_HOST

def generate_pairing(season, location, preferences):
    payload = {
        "season": season,
        "location": location,
        "preferences": preferences
    }
    response = requests.post(f"{OLLAMA_HOST}/api/recommendations", json=payload)
    return response.json()
