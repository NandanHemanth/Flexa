# import streamlit as st
# import json
# import os
# import subprocess

# # Database setup
# DB_FILE = "splitwise_data.json"

# def init_db():
#     if not os.path.exists(DB_FILE):
#         with open(DB_FILE, "w") as f:
#             json.dump({"users": [], "expenses": []}, f)

# init_db()

# # Load database
# def load_db():
#     with open(DB_FILE, "r") as f:
#         return json.load(f)

# # Save database
# def save_db(data):
#     with open(DB_FILE, "w") as f:
#         json.dump(data, f, indent=4)

# # Add user
# def add_user(name):
#     data = load_db()
#     user_id = len(data["users"]) + 1
#     data["users"].append({"id": user_id, "name": name})
#     save_db(data)

# def get_users():
#     return load_db()["users"]

# # Add expense
# def add_expense(payer_id, amount, description, participants):
#     data = load_db()
#     data["expenses"].append({
#         "payer_id": payer_id,
#         "amount": amount,
#         "description": description,
#         "participants": participants
#     })
#     save_db(data)

# def get_expenses():
#     return load_db()["expenses"]

# # Streamlit UI
# st.title("💸 Flexa - Bill Splitting System")
# st.sidebar.header("Manage Users")
# new_user = st.sidebar.text_input("Add a new user")
# if st.sidebar.button("Add User"):
#     add_user(new_user)
#     st.sidebar.success(f"User {new_user} added!")

# users = get_users()
# user_dict = {user["id"]: user["name"] for user in users}

# st.sidebar.header("Add Expense")
# selected_payer = st.sidebar.selectbox("Who paid?", options=user_dict.keys(), format_func=lambda x: user_dict[x])
# amount = st.sidebar.number_input("Amount", min_value=0.01, format="%.2f")
# description = st.sidebar.text_input("Description")
# selected_participants = st.sidebar.multiselect("Who participated?", options=user_dict.keys(), format_func=lambda x: user_dict[x])
# if st.sidebar.button("Add Expense"):
#     add_expense(selected_payer, amount, description, selected_participants)
#     st.sidebar.success("Expense added!")

# st.header("📊 Expense History")
# expenses = get_expenses()
# for expense in expenses:
#     payer_name = user_dict.get(expense["payer_id"], "Unknown")
#     participants = ", ".join([user_dict.get(uid, "Unknown") for uid in expense["participants"]])
#     st.write(f"💰 {payer_name} paid ${expense['amount']:.2f} for {expense['description']} | Shared with: {participants}")


# # Run OCR Script for bill scanning
# if st.button("Scan Bill with Gemini AI"):
#     subprocess.run(["python", "ocr_gemini.py"])

import streamlit as st
import json
import os

# --- Database Setup ---
DB_FILE = "splitwise_data.json"

def init_db():
    """Initialize the database file with default users if empty."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"users": [], "expenses": []}, f)

    # Load the database
    data = load_db()

    # Prepopulate with test users if empty
    if not data["users"]:
        default_users = [
            {"id": 1, "name": "Sarah"},
            {"id": 2, "name": "Timmy"},
            {"id": 3, "name": "Nandan"}
        ]
        data["users"].extend(default_users)
        save_db(data)

init_db()

def load_db():
    """Load data from JSON database."""
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    """Save data back to the JSON database."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(name):
    """Add a new user to the database."""
    data = load_db()
    user_id = len(data["users"]) + 1
    data["users"].append({"id": user_id, "name": name})
    save_db(data)
    print("✅ User Added:", data)  # Debugging Output

def get_users():
    """Get list of users from the database."""
    data = load_db()
    print("📂 Users in DB:", data["users"])  # Debugging Output
    return data["users"]

def add_expense(payer_id, amount, description, participants):
    """Add a new expense to the database."""
    data = load_db()
    data["expenses"].append({
        "payer_id": payer_id,
        "amount": amount,
        "description": description,
        "participants": participants
    })
    save_db(data)
    print("💰 Expense Added:", data)  # Debugging Output

def get_expenses():
    """Get list of expenses from the database."""
    data = load_db()
    print("📂 Expenses in DB:", data["expenses"])  # Debugging Output
    return data["expenses"]

# --- Streamlit UI ---
st.title("💸 Flexa - Bill Splitting System")

# Sidebar: Add User
st.sidebar.header("👥 Manage Users")
new_user = st.sidebar.text_input("Enter new user name")
if st.sidebar.button("Add User"):
    add_user(new_user)
    st.sidebar.success(f"✅ User {new_user} added!")

# Load Users
users = get_users()
user_dict = {user["id"]: user["name"] for user in users}

# Sidebar: Add Expense
st.sidebar.header("💰 Add Expense")
selected_payer = st.sidebar.selectbox("Who paid?", options=user_dict.keys(), format_func=lambda x: user_dict[x])
amount = st.sidebar.number_input("Amount", min_value=0.01, format="%.2f")
description = st.sidebar.text_input("Expense Description")
selected_participants = st.sidebar.multiselect("Who participated?", options=user_dict.keys(), format_func=lambda x: user_dict[x])

if st.sidebar.button("Add Expense"):
    add_expense(selected_payer, amount, description, selected_participants)
    st.sidebar.success("✅ Expense added!")

# Display Users
st.subheader("👥 User List")
for user in users:
    st.write(f"👤 {user['name']} (ID: {user['id']})")

# Display Expenses
st.subheader("📊 Expense History")
expenses = get_expenses()
for expense in expenses:
    payer_name = user_dict.get(expense["payer_id"], "Unknown")
    participants = ", ".join([user_dict.get(uid, "Unknown") for uid in expense["participants"]])
    st.write(f"💰 {payer_name} paid ${expense['amount']:.2f} for {expense['description']} | Shared with: {participants}")
