import streamlit as st
from PIL import Image
from utils.nutritionx_api import fetch_nutrition_data
import plotly.graph_objects as go
from utils.chatbot import ask_nutrition_bot

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
            # Accumulators for total nutrients
            total_calories = 0
            total_protein = 0
            total_fat = 0
            total_carbs = 0

            food_names = []
            food_calories = []
            food_proteins = []
            food_carbs = []
            food_fats = []

            for food in data['foods']:
                total_calories += food['nf_calories']
                total_protein += food['nf_protein']
                total_carbs += food['nf_total_carbohydrate']
                total_fat += food['nf_total_fat']
                
                food_names.append(food['food_name'].title())
                food_calories.append(food['nf_calories'])
                food_proteins.append(food['nf_protein'])
                food_carbs.append(food['nf_total_carbohydrate'])
                food_fats.append(food['nf_total_fat'])
                
            # Pie chart for macronutrient distribution
            st.subheader("🍩 Macronutrient Breakdown (Pie Chart)")

            pie_fig = go.Figure(data=[go.Pie(labels=['Protein', 'Carbs', 'Fat'],
                                            values=[total_protein, total_carbs, total_fat],
                                            hole=0.4)])

            st.plotly_chart(pie_fig, use_container_width=True)

            # Bar chart for calorie per item
            st.subheader("📊 Calories Per Food Item")

            bar_fig = go.Figure(data=[go.Bar(x=food_names, y=food_calories, marker_color='indianred')])
            bar_fig.update_layout(xaxis_title="Food Item", yaxis_title="Calories")

            st.plotly_chart(bar_fig, use_container_width=True)
            
            #Protein per food
            st.subheader("💪 Protein Per Food Item (g)")
            protein_fig = go.Figure(data=[go.Bar(x=food_names, y=food_proteins, marker_color='seagreen')])
            protein_fig.update_layout(xaxis_title="Food Item", yaxis_title="Protein (g)")
            st.plotly_chart(protein_fig, use_container_width=True)
            
            #Carbs per food
            st.subheader("🍞 Carbs Per Food Item (g)")
            carbs_fig = go.Figure(data=[go.Bar(x=food_names, y=food_carbs, marker_color='dodgerblue')])
            carbs_fig.update_layout(xaxis_title="Food Item", yaxis_title="Carbohydrates (g)")
            st.plotly_chart(carbs_fig, use_container_width=True)

            #Fat per food
            st.subheader("🧈 Fats Per Food Item (g)")
            fat_fig = go.Figure(data=[go.Bar(x=food_names, y=food_fats, marker_color='goldenrod')])
            fat_fig.update_layout(xaxis_title="Food Item", yaxis_title="Fat (g)")
            st.plotly_chart(fat_fig, use_container_width=True)



        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a meal description.")

# --- Chatbot Section ---
st.header("💬 Chat with Nutrition Bot")

user_query = st.text_input("Ask a nutrition-related question")

if st.button("Ask Bot"):
    if user_query.strip():
        with st.spinner("🤖 Thinking..."):
            try:
                response = ask_nutrition_bot(user_query)
                st.markdown("### 🤖 Bot Response")
                st.markdown(f"> {response}")
            except Exception as e:
                st.error(f"❌ {e}")
    else:
        st.warning("Please enter a question for the chatbot.")


