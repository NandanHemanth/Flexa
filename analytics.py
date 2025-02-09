import streamlit as st
import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import calendar
from streamlit_lottie import st_lottie
import requests

# Ensure database folder exists
os.makedirs("./database", exist_ok=True)

# Load user profile data
PROFILE_PATH = "./database/user_profiles.json"
WORKOUT_HISTORY_PATH = "./database/workout_history.json"
STREAK_TRACKER_PATH = "./database/streak_tracker.json"

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def generate_meal_plan():
    return {
        "Monday": {"Breakfast": "Oatmeal with berries and nuts", "Lunch": "Grilled chicken salad", "Snack": "Greek yogurt", "Dinner": "Salmon with vegetables"},
        "Tuesday": {"Breakfast": "Scrambled eggs and toast", "Lunch": "Quinoa and avocado bowl", "Snack": "Protein smoothie", "Dinner": "Grilled steak and sweet potatoes"},
        "Wednesday": {"Breakfast": "Pancakes with almond butter", "Lunch": "Grilled salmon with rice", "Snack": "Mixed nuts", "Dinner": "Turkey stir-fry"},
        "Thursday": {"Breakfast": "Greek yogurt with granola", "Lunch": "Chicken wrap", "Snack": "Fruit salad", "Dinner": "Lentil soup and brown rice"},
        "Friday": {"Breakfast": "Peanut butter toast", "Lunch": "Tuna salad sandwich", "Snack": "Carrots and hummus", "Dinner": "Baked chicken and quinoa"}
    }

def generate_workout_plan():
    return {
        "Monday": "Upper Body Strength Training",
        "Tuesday": "Cardio & Core Workout",
        "Wednesday": "Leg Day - Squats, Deadlifts",
        "Thursday": "Active Recovery - Yoga, Stretching",
        "Friday": "Full Body HIIT Routine"
    }

def display_calendar(meal_plan, workout_plan, streak_tracker):
    st.subheader("📅 Weekly Plan Overview")
    days = list(meal_plan.keys())

    if "streak_tracker" not in st.session_state:
        st.session_state.streak_tracker = streak_tracker
    
    streak_score = 0
    for day in days:
        checked = st.checkbox(f"✅ {day} Completed", value=st.session_state.streak_tracker.get(day, False), key=day)
        st.session_state.streak_tracker[day] = checked
    
    streak_score = sum(1 for day in days if st.session_state.streak_tracker.get(day, False))
    save_json(STREAK_TRACKER_PATH, st.session_state.streak_tracker)
    
    st.write(f"🔥 **Current Streak Score:** {streak_score} days")
    
    calendar_df = pd.DataFrame({
        "Day": days,
        "Breakfast": [meal_plan[day]["Breakfast"] for day in days],
        "Lunch": [meal_plan[day]["Lunch"] for day in days],
        "Snack": [meal_plan[day]["Snack"] for day in days],
        "Dinner": [meal_plan[day]["Dinner"] for day in days],
        "Workout": [workout_plan[day] for day in days]
    })
    st.dataframe(calendar_df)

def display_graphs(workout_history):
    df = pd.DataFrame(workout_history)
    if df.empty:
        st.warning("No workout data available.")
        return
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")
    
    # Calories burnt over time
    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["calories"], marker="o", linestyle="-", label="Calories Burnt")
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories Burnt")
    ax.set_title("Calories Burnt Over Time")
    ax.legend()
    st.pyplot(fig)
    
    # Exercise score trend
    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["score"], marker="s", linestyle="--", color="green", label="Exercise Score")
    ax.set_xlabel("Date")
    ax.set_ylabel("Form Score (%)")
    ax.set_title("Exercise Score Progress")
    ax.legend()
    st.pyplot(fig)

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    # Load animations
    meal_animation = load_lottie_url("https://lottie.host/76c6d628-9e39-4099-b55d-27b5489ee557/q1GGTjMa0O.json")
    workout_animation = load_lottie_url("https://lottie.host/9e72d50f-9219-4e27-970c-95d7d604d1ba/3BNR1SE38T.json")

    # Load user data
    user_profiles = load_json(PROFILE_PATH)
    workout_history = load_json(WORKOUT_HISTORY_PATH)
    streak_tracker = load_json(STREAK_TRACKER_PATH)

    if not user_profiles:
        st.error("No user profiles found. Please create your profile in 'Me, Myself & Flex'.")
    else:
        user_id = list(user_profiles.keys())[0]  # Assuming first user for now
        user_data = user_profiles[user_id]
        
        st.title("🥑 Munch & Crunch - Personalized Lifestyle Plan")
        # st_lottie(meal_animation, height=250, key="meal")
        
        meal_plan = generate_meal_plan()
        workout_plan = generate_workout_plan()
        
        display_calendar(meal_plan, workout_plan, streak_tracker)
        
        st.subheader("📊 Your Progress")
        # st_lottie(workout_animation, height=250, key="workout")
        display_graphs(workout_history)

        st.success("Your customized 5-day meal & workout plan is ready! 🥗💪")
