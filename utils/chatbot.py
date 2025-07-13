import os
import requests
import json
from dotenv import load_dotenv

# Load your .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Optional (for usage tracking on openrouter.ai rankings)
SITE_URL = "http://localhost"      # Change to your site if deployed
SITE_TITLE = "Nutrition Chatbot"   # Custom project name

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1:free"

def ask_nutrition_bot(user_query):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_TITLE
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful nutritionist who gives clear, friendly and accurate advice about food, diet, and health."},
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"OpenRouter API Error: {response.status_code}, {response.text}")


#  CLI Mode (optional testing from terminal)
# if __name__ == "__main__":
#     print("💬 Nutrition Bot (DeepSeek via OpenRouter)")
#     print("Type 'exit' to quit\n")
#     while True:
#         query = input("You: ")
#         if query.lower() in ["exit", "quit"]:
#             break
#         try:
#             reply = ask_nutrition_bot(query)
#             print("Bot:", reply)
#         except Exception as e:
#             print("❌ Error:", e)
