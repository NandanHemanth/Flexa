import streamlit as st
import json
import os
from google import genai
from PIL import Image
import pytesseract
from dotenv import load_dotenv

# --- Load API Key from .env ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

# --- OCR Function (Extract Text from Image) ---
def extract_text_from_image(image_path):
    """Extracts text from an image using Tesseract OCR."""
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

# --- Gemini API Processing Function ---
def process_with_gemini(text):
    """Send extracted OCR text to Gemini AI for structured JSON output."""
    
    prompt = f"""
    Extract structured data from this receipt and return it in JSON format.
    
    Use this JSON schema:
    {{
        "restaurant_name": str,
        "date": str,
        "items": [
            {{
                "name": str,
                "quantity": int,
                "price": float
            }}
        ],
        "food_tax": float,
        "sales_tax": float,
        "tip": float,
        "total": float
    }}

    Here is the raw extracted text from the receipt:
    ```
    {text}
    ```
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    try:
        structured_data = json.loads(response.text)
        print("✅ Gemini AI Response:", structured_data)  # Debugging Output
        return structured_data
    except json.JSONDecodeError:
        return {"error": "Failed to parse Gemini AI response"}

# --- Streamlit UI ---
st.title("🧾 OCR Bill Scanner with Gemini AI")
uploaded_file = st.file_uploader("📄 Upload your bill image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image_path = os.path.join("./uploads", uploaded_file.name)
    os.makedirs("./uploads", exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="🧾 Uploaded Bill", use_column_width=True)

    # Extract text from the image
    extracted_text = extract_text_from_image(image_path)
    st.subheader("🔍 Extracted Text from Image")
    st.text(extracted_text)  # Display raw text from OCR for debugging

    # Process the extracted text with Gemini AI
    st.write("🤖 Processing with Gemini AI...")
    structured_data = process_with_gemini(extracted_text)

    # Display structured JSON output
    st.subheader("📊 Extracted Bill Details")
    st.json(structured_data)

    # Save output as JSON file in `/database`
    database_path = "./database"
    os.makedirs(database_path, exist_ok=True)
    json_file_path = os.path.join(database_path, f"bill_{uploaded_file.name}.json")

    with open(json_file_path, "w") as json_file:
        json.dump(structured_data, json_file, indent=4)

    st.success(f"✅ Data extracted and saved in `{json_file_path}`!")
