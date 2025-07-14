# 🥗 Nutrition Analysis and Chatbot Assistant

An intelligent and interactive Streamlit web app that allows users to analyze the nutrition content of their meals and chat with an AI nutritionist for dietary advice.

> Built as an internship project by **Aman Singh**, this app combines data analysis with AI to help users make informed food choices.

---

## 🚀 Features

✅ Analyze meals using **Nutritionix API**  
✅ Interactive chatbot powered by **DeepSeek R1 via OpenRouter API**  
✅ Nutritional visualizations with **Plotly**  
✅ Compare your nutrition intake with **Recommended Daily Values (RDV)**  
✅ Download your **nutrition summary as a `.txt` file**  
✅ Smooth **chat experience** with persistent chat history  

---

## ⚙️ APIs Used

### 1. [Nutritionix API](https://developer.nutritionix.com/)
Used for retrieving nutritional information for meals described by the user.

- **Required keys**: `NUTRITIONIX_APP_ID`, `NUTRITIONIX_API_KEY`

### 2. [OpenRouter API](https://openrouter.ai/)
Used to connect to **DeepSeek R1** for nutrition-related chatbot queries.

- **Required key**: `OPENROUTER_API_KEY`

---

## 🔐 Setup Instructions

### Step 1: Clone the repository

> git clone https://github.com/your-username/nutrition-analysis-chatbot.git

> cd nutrition-analysis-chatbot


### Step 2: Create a .env file
Create a .env file in the root directory:

>NUTRITIONIX_APP_ID=your_app_id_here

>NUTRITIONIX_API_KEY=your_nutritionix_key_here

>OPENROUTER_API_KEY=your_openrouter_key_here


### Step 3: Install dependencies

>pip install -r requirements.txt


### Step 4: Run the application

>streamlit run app.py


---

## 📊 Visualizations

Pie chart: Macronutrient distribution (protein, carbs, fat)

Bar charts: Per-item calories, protein, carbs, fat

Horizontal comparison: User intake vs Recommended Daily Values (RDV)

---

### 🧠 Technologies Used

Streamlit — UI framework

OpenRouter + DeepSeek R1 — Chatbot engine

Nutritionix — Food data

Plotly — Charts and graphs

Python 3.10+

---

## 🔜 Future Work

**Image-based food input support**

---
## 👤 Author
Aman Singh
BTech CSE, Graphic Era University
Intern at O7 Services Pvt. Ltd.

📧 Email: [rajputaman6554@gmail.com]