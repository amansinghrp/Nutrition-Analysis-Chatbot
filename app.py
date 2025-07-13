import streamlit as st
from PIL import Image
from utils.nutritionx_api import fetch_nutrition_data
# Page config
st.set_page_config(page_title="Nutrition Analyzer & Chatbot", layout="wide")

# Title
st.title("🥗 Nutrition Analysis and Chatbot Assistant")

# --- Input Section ---
st.header("📥 Input your meal")

# Text input
food_input = st.text_area("Describe your meal (e.g., '2 boiled eggs and 1 cup rice')", height=100)

# --- Nutrition Analysis Placeholder ---
if st.button("Analyze Nutrition"):
    if food_input:
        try:
            data = fetch_nutrition_data(food_input)
            st.subheader("🍽 Nutrition Analysis")

            for food in data['foods']:
                st.markdown(f"### 🥘 {food['food_name'].title()}")
                st.write(f"Calories: {food['nf_calories']} kcal")
                st.write(f"Protein: {food['nf_protein']} g")
                st.write(f"Carbs: {food['nf_total_carbohydrate']} g")
                st.write(f"Fat: {food['nf_total_fat']} g")
                st.write("---")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a meal description.")

# --- Chatbot Section ---
st.header("💬 Chat with Nutrition Bot")
user_query = st.text_input("Ask a nutrition-related question")
if st.button("Ask Bot"):
    if user_query:
        st.subheader("🤖 Bot Response")
        st.info("Response will be generated using OpenAI GPT API.")
    else:
        st.error("Please enter a question for the chatbot.")
