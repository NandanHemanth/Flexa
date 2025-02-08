import streamlit as st
import subprocess
import time
import json
import os
from streamlit_lottie import st_lottie
import requests
# from flexa_bill import process_with_gemini

# --- Page Config ---
st.set_page_config(page_title="Flexa", page_icon="🍑", layout="wide")

# Ensure database folder exists
os.makedirs("./database", exist_ok=True)

# Function to load existing user data
def load_user_data():
    file_path = "./database/user_profiles.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

# Function to save user data
def save_user_data(user_data):
    file_path = "./database/user_profiles.json"
    
    existing_data = load_user_data()
    
    # Auto-increment user ID
    new_user_id = len(existing_data) + 1
    existing_data[new_user_id] = user_data
    
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)
    
    return new_user_id
# --- Function to Fetch Lottie Animations ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Lottie Animations ---
splitwise_animation = load_lottie_url("https://lottie.host/5f97f66c-b96a-493c-9d98-e61c49fce1b3/AEZhJ3cU05.json")


# --- Sidebar ---
st.sidebar.title("🔥 **Flexa Navigation**")
section = st.sidebar.radio("Select a Section:", [
    "📝 Me, Myself & Flex",
    "💪 Flexa-Tron 3000",
    "🥑 Munch & Crunch",
    "💸 Flexa"
])

# --- Main Page ---
st.title("**Welcome to Flexa!** 🚀")
st.write("### Lifestyle SUPER-App with meme energy! 🔥")

if section == "📝 Me, Myself & Flex":
    st.header("📝 Me, Myself & Flex")
    st.write("*Because your profile deserves some gains too!* 😎")

    with st.form("user_profile_form"):
        st.subheader("👤 Personal Details")
        name = st.text_input("Full Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter your email")

        st.subheader("🥗 Health & Fitness")
        dietary_restrictions = st.text_area("Dietary Restrictions", placeholder="Any allergies or diet plans?")
        
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)
        with col2:
            weight = st.number_input("Weight (kg)", min_value=20, max_value=300, step=1)

        st.subheader("🎯 Goals & Activity")
        goal_options = ["Bulking 🏋️", "Cutting 🔥", "Lean Bulk 💪", "Maintain ⚖️", "Flexibility & Mobility 🤸"]
        goal = st.selectbox("Fitness Goal", goal_options)

        activity_options = ["Sedentary (little to no exercise)", "Lightly active (1-3 days/week)", 
                            "Moderately active (3-5 days/week)", "Very active (6-7 days/week)", 
                            "Super active (Athlete level)"]
        activity_level = st.selectbox("Activity Level", activity_options)

        submit_button = st.form_submit_button("Save Profile", type="primary")

    if submit_button:
        user_data = {
            "name": name,
            "email": email,
            "dietary_restrictions": dietary_restrictions,
            "height": height,
            "weight": weight,
            "goal": goal,
            "activity_level": activity_level
        }

        user_id = save_user_data(user_data)
        st.success(f"Profile Saved! 🚀 (User ID: {user_id})")
    
elif section == "💪 Flexa-Tron 3000":
    st.header("💪 Flexa-Tron 3000")
    st.write("*An AI trainer that doesn’t skip leg day!* 💪🔥")

    st.sidebar.info("💡 Stay consistent! Track your workouts and diet to maximize results.")
    
elif section == "🥑 Munch & Crunch":
    st.header("🥑 Munch & Crunch")
    st.write("*Diet so good, even Gordon Ramsay won’t yell at you!* 🍔🥗")
    
elif section == "💸 Flexa":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💸 Flexa - Bill Splitting System")

        # Toggle for showing file uploader
        scan_bill = st.button("🧾 Scan Bill with FlexaAI", type="primary")

        if scan_bill:
            uploaded_file = st.file_uploader("📄 Upload your bill image", type=["png", "jpg", "jpeg"])


    with col2:
        st_lottie(splitwise_animation, height=300, key="splitwise")

# Footer for all pages - Centered
st.markdown("""
    <style>
        .footer {
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 0px;
            font-size: 16px;
        }
    </style>
    <div class='footer'>
        Made by Flexa with ❣️
    </div>
""", unsafe_allow_html=True) 



        

