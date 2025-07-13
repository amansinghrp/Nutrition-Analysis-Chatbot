import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("NUTRITIONIX_APP_ID")
APP_KEY = os.getenv("NUTRITIONIX_APP_KEY")

def fetch_nutrition_data(query):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "query": query,
        "timezone": "Asia/Kolkata"
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Nutritionix API error: {response.status_code}, {response.text}")
