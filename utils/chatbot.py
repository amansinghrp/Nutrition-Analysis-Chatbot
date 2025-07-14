import os
import requests
import json
from dotenv import load_dotenv
import random

fallbacks = [
    "🤖 Hmm, I didn't catch that. Mind trying again?",
    "⚠️ Looks like I lost my train of thought. Could you rephrase that?",
    "🙃 Something went wrong on my end. Try again?"
]
# Load your .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

SITE_URL = "http://localhost"      
SITE_TITLE = "Nutrition Chatbot"   

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1:free"

def ask_nutrition_bot(question, nutrition_info=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_TITLE
    }
    context = "You are a helpful nutritionist. Respond with friendly and useful suggestions."

    if nutrition_info:
        context += f"\n\nHere is the user's current nutritional data:\n{nutrition_info}"

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        try:
            reply = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            if not reply or len(reply) < 30:
                return random.choice(fallbacks)
            return reply
        except (KeyError, IndexError):
                return "⚠️ Unexpected response format from the model. Please try again."
    else:
        return f"❌ API Error {response.status_code}: {response.text}"


##  CLI Mode (optional testing from terminal)
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
