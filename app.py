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

# --- Custom CSS for Gradient Background ---
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            margin: 0;
            height: 100vh;
            width: 100vw;
            position: fixed;
            top: 0;
            left: 0;
            z-index: -1;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Function to Fetch Lottie Animations ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Lottie Animations ---
profile_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_5wXrYB.json")
trainer_animation = load_lottie_url("https://assets3.lottiefiles.com/private_files/lf30_1vqeqvdd.json")
diet_animation = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_hl5n0bwb.json")
splitwise_animation = load_lottie_url("https://lottie.host/5f97f66c-b96a-493c-9d98-e61c49fce1b3/AEZhJ3cU05.json")

# --- Database Setup ---
DB_FILE = "splitwise_data.json"

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"users": [], "expenses": []}, f)

init_db()

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(name):
    data = load_db()
    user_id = len(data["users"]) + 1
    data["users"].append({"id": user_id, "name": name})
    save_db(data)

def get_users():
    return load_db()["users"]

def add_expense(payer_id, amount, description, participants):
    data = load_db()
    data["expenses"].append({
        "payer_id": payer_id,
        "amount": amount,
        "description": description,
        "participants": participants
    })
    save_db(data)

def get_expenses():
    return load_db()["expenses"]

# --- Sidebar ---
st.sidebar.title("🔥 **Flexa Navigation**")
section = st.sidebar.radio("Select a Section:", [
    "📝 Me, Myself & Flex",
    "💪 Flexa-Tron 3000",
    "🥑 Munch & Crunch",
    "💸 Flexa"
])

# --- Main Page ---
st.title("😂 **Welcome to Flexa!** 🚀")
st.write("### The ultimate lifestyle app with meme energy! 🔥")

if section == "📝 Me, Myself & Flex":
    st.header("📝 Me, Myself & Flex")
    st.write("*Because your profile deserves some gains too!* 😎")
    
elif section == "💪 Flexa-Tron 3000":
    st.header("💪 Flexa-Tron 3000")
    st.write("*An AI trainer that doesn’t skip leg day!* 💪🔥")
    
elif section == "🥑 Munch & Crunch":
    st.header("🥑 Munch & Crunch")
    st.write("*Diet so good, even Gordon Ramsay won’t yell at you!* 🍔🥗")
    
elif section == "💸 Flexa":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💸 Flexa - Bill Splitting System")

        # Toggle for showing file uploader
        scan_bill = st.button("🧾 Scan Bill with FlexaAI", key="primary")

        if scan_bill:
            uploaded_file = st.file_uploader("📄 Upload your bill image", type=["png", "jpg", "jpeg"])

            if uploaded_file:
                image_path = os.path.join("./uploads", uploaded_file.name)
                os.makedirs("./uploads", exist_ok=True)

                # Save the uploaded file
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Show uploaded image
                st.image(image_path, caption="🧾 Uploaded Bill", use_column_width=True)

                # Process Bill with Gemini AI
                st.write("🤖 Processing with FlexaAI...")
                from flexa_bill import process_with_gemini  # Import function dynamically
                structured_data = process_with_gemini(image_path)

                # Display structured JSON output
                st.subheader("📊 Extracted Bill Details")
                st.json(structured_data)

                # Save output as JSON file in /database
                database_path = "./database"
                os.makedirs(database_path, exist_ok=True)  # Ensure directory exists
                json_file_path = os.path.join(database_path, f"bill_{uploaded_file.name}.json")

                with open(json_file_path, "w") as json_file:
                    json.dump(structured_data, json_file, indent=4)

                st.success(f"✅ Data extracted and saved in `{json_file_path}`!")

        st.subheader("👥 Manage Users")
        new_user = st.text_input("Add a new user")
        if st.button("➕ Add User"):
            add_user(new_user)
            st.success(f"User {new_user} added! 🎉")

        users = get_users()
        user_dict = {user["id"]: user["name"] for user in users}

        st.subheader("💰 Add Expense")
        selected_payer = st.selectbox("Who paid?", options=user_dict.keys(), format_func=lambda x: user_dict[x])
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        description = st.text_input("Description")
        selected_participants = st.multiselect("Who participated?", options=user_dict.keys(), format_func=lambda x: user_dict[x])

        if st.button("💸 Add Expense"):
            add_expense(selected_payer, amount, description, selected_participants)
            st.success("Expense added! ✅")

        st.subheader("📊 Expense History")
        expenses = get_expenses()
        for expense in expenses:
            payer_name = user_dict.get(expense["payer_id"], "Unknown")
            participants = ", ".join([user_dict.get(uid, "Unknown") for uid in expense["participants"]])
            st.write(f"💰 {payer_name} paid **${expense['amount']:.2f}** for **{expense['description']}** | Shared with: {participants}")

    with col2:
        st_lottie(splitwise_animation, height=300, key="splitwise")



        

