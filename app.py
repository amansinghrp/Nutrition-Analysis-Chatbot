import streamlit as st
from PIL import Image
from utils.nutritionx_api import fetch_nutrition_data
import plotly.graph_objects as go
from utils.chatbot import ask_nutrition_bot
import pandas as pd

# Page config
st.set_page_config(page_title="Nutrition Analyzer & Chatbot", layout="wide")

# Title
st.title("🥗 Nutrition Analysis and Chatbot Assistant")

# --- Session State Initialization ---
if "food_input" not in st.session_state:
    st.session_state.food_input = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "nutrition_summary" not in st.session_state:
    st.session_state.nutrition_summary = ""
if "nutrition_analyzed" not in st.session_state:
    st.session_state.nutrition_analyzed = False
if "nutrition_data" not in st.session_state:
    st.session_state.nutrition_data = {}

# --- Input Section ---
st.header("📥 Input your meal")
food_input = st.text_area("Describe your meal", 
                          height=100, 
                          value=st.session_state.food_input)
analyze_button = st.button("Analyze Nutrition")

# --- Nutrition Analysis ---
if analyze_button or st.session_state.nutrition_analyzed:
    if food_input.strip():
        st.session_state.food_input = food_input
        try:
            if analyze_button:
                data = fetch_nutrition_data(food_input)
                st.session_state.nutrition_data = data
                st.session_state.nutrition_analyzed = True
            else:
                data = st.session_state.nutrition_data

            st.subheader("🍽 Nutrition Analysis")

            # Convert to DataFrame
            df_nutrition = pd.DataFrame([{
                "Food Item": food['food_name'].title(),
                "Calories (kcal)": food['nf_calories'],
                "Protein (g)": food['nf_protein'],
                "Carbs (g)": food['nf_total_carbohydrate'],
                "Fat (g)": food['nf_total_fat']
            } for food in data['foods']])

            # Display table
            st.subheader("🥘 Food Item Breakdown")
            st.dataframe(df_nutrition, use_container_width=True)

            # Accumulators
            total_calories = sum(f['nf_calories'] for f in data['foods'])
            total_protein = sum(f['nf_protein'] for f in data['foods'])
            total_carbs = sum(f['nf_total_carbohydrate'] for f in data['foods'])
            total_fat = sum(f['nf_total_fat'] for f in data['foods'])

            # Build per-item breakdown
            item_lines = []
            for food in data['foods']:
                name = food['food_name'].title()
                cal = food['nf_calories']
                protein = food['nf_protein']
                carbs = food['nf_total_carbohydrate']
                fat = food['nf_total_fat']
                item_lines.append(f"- {name}: {cal:.0f} kcal | {protein:.1f}g protein, {carbs:.1f}g carbs, {fat:.1f}g fat")

            # Build full summary text
            st.session_state.nutrition_summary = (
                f"The user enquired about: {food_input.strip()}\n\n"
                f"🔢 Total nutrition:\n"
                f"- Calories: {total_calories:.0f} kcal\n"
                f"- Protein: {total_protein:.1f} g\n"
                f"- Carbohydrates: {total_carbs:.1f} g\n"
                f"- Fat: {total_fat:.1f} g\n\n"
                f"📋 Per-item breakdown:\n" +
                "\n".join(item_lines)
            )

            # ✅ Download Button
            st.download_button(
                label="📥 Download Nutrition Summary",
                data=st.session_state.nutrition_summary,
                file_name="nutrition_summary.txt",
                mime="text/plain"
            )

            # ✅ Recommended Daily Comparison
            st.subheader("📊 Recommended Daily Intake Comparison")

            recommended_values = {
                "Calories": 2000,
                "Protein": 50,
                "Carbs": 275,
                "Fat": 70
            }
            
            df_comparison = pd.DataFrame({
                "Nutrient": ["Calories", "Protein (g)", "Carbs (g)", "Fat (g)"],
                "Your Intake": [total_calories, total_protein, total_carbs, total_fat],
                "Recommended": [
                    recommended_values["Calories"],
                    recommended_values["Protein"],
                    recommended_values["Carbs"],
                    recommended_values["Fat"]
                ]
            })

            st.dataframe(df_comparison, use_container_width=True)

            st.subheader("📈 Intake vs Recommended (Visual Comparison)")

            nutrients = ["Calories", "Protein", "Carbs", "Fat"]
            your_vals = [total_calories, total_protein, total_carbs, total_fat]
            rec_vals = [recommended_values[n] for n in nutrients]

            fig = go.Figure()

            fig.add_trace(go.Bar(
                y=nutrients,
                x=your_vals,
                name='Your Intake',
                orientation='h',
                marker_color='green'
            ))
            fig.add_trace(go.Bar(
                y=nutrients,
                x=rec_vals,
                name='Recommended',
                orientation='h',
                marker_color='gray'
            ))

            fig.update_layout(barmode='group', xaxis_title="Amount", yaxis_title="Nutrient")

            st.plotly_chart(fig, use_container_width=True)


            # Individual food breakdowns
            food_names = [f['food_name'].title() for f in data['foods']]
            food_calories = [f['nf_calories'] for f in data['foods']]
            food_proteins = [f['nf_protein'] for f in data['foods']]
            food_carbs = [f['nf_total_carbohydrate'] for f in data['foods']]
            food_fats = [f['nf_total_fat'] for f in data['foods']]

            # Visualizations
            st.subheader("🍩 Macronutrient Breakdown (Pie Chart)")
            pie_fig = go.Figure(data=[go.Pie(
                labels=['Protein', 'Carbs', 'Fat'],
                values=[total_protein, total_carbs, total_fat],
                hole=0.4)])
            st.plotly_chart(pie_fig, use_container_width=True)

            # Calories per item
            st.subheader("📊 Calories Per Food Item")
            bar_fig = go.Figure(data=[go.Bar(x=food_names, y=food_calories, marker_color='indianred')])
            bar_fig.update_layout(xaxis_title="Food Item", yaxis_title="Calories")
            st.plotly_chart(bar_fig, use_container_width=True)

            # Protein per item
            st.subheader("💪 Protein Per Food Item (g)")
            protein_fig = go.Figure(data=[go.Bar(x=food_names, y=food_proteins, marker_color='seagreen')])
            protein_fig.update_layout(xaxis_title="Food Item", yaxis_title="Protein (g)")
            st.plotly_chart(protein_fig, use_container_width=True)

            # Carbs per item
            st.subheader("🍞 Carbs Per Food Item (g)")
            carbs_fig = go.Figure(data=[go.Bar(x=food_names, y=food_carbs, marker_color='dodgerblue')])
            carbs_fig.update_layout(xaxis_title="Food Item", yaxis_title="Carbohydrates (g)")
            st.plotly_chart(carbs_fig, use_container_width=True)

            # Fats per item
            st.subheader("🧈 Fats Per Food Item (g)")
            fat_fig = go.Figure(data=[go.Bar(x=food_names, y=food_fats, marker_color='goldenrod')])
            fat_fig.update_layout(xaxis_title="Food Item", yaxis_title="Fat (g)")
            st.plotly_chart(fat_fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please enter a meal description.")

# --- Chatbot Section ---
st.header("💬 Chat with Nutrition Bot")

# --- Display Chat History using chat_message ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask a nutrition-related question"):
    # Save user input to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot reply
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            try:
                response = ask_nutrition_bot(
                    prompt,
                    nutrition_info=st.session_state.get("nutrition_summary", "")
                )
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"❌ {e}")
