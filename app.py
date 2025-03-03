import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import io
import base64

# Gemini API settings
API_KEY = "AIzaSyBNGL46z-zi1Uvrpkd2cafjh8D5aeXQOWQ"  # Replace with your actual key
genai.configure(api_key=API_KEY)

# Create upload folder if needed
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(
    page_title="AI-Powered Skin Disease Classification",
    layout="wide",  # Use the entire screen width
)

# 2) Inject Custom CSS to reduce padding and control layout
st.markdown(
    """
    <style>
    /* Reduce padding around the main container */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1000px; /* You can adjust this width as needed */
        margin: auto;      /* Center the container horizontally */
        
    }

    /* Make the background an animated gradient (example) */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-size: 30px;
        
    }

    @keyframes gradientBG {
        0%   { background-position: 0%   50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0%   50%; }
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ---- Streamlit UI ----
st.title("AI-Powered Skin Disease Classification")

# Upload widget: Accept only image files
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read file as bytes and display the image
    file_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(file_bytes))
    st.image(
    image, 
    caption="Uploaded Image",
    use_container_width=True  # <--- Replace use_column_width=True with this
)


    # Optionally save the uploaded image to disk
    filename = uploaded_file.name
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(file_bytes)

    # Classify button to trigger processing
    if st.button("Classify"):
        with st.spinner("Classifying..."):
            try:
                # Load the Gemini AI model
                model = genai.GenerativeModel("gemini-1.5-flash")

                # Optionally encode the image in base64 (if needed by your API)
                # image_base64 = base64.b64encode(file_bytes).decode('utf-8')

                # The Gemini API here expects a PIL image object within a list
                response = model.generate_content([image])

                if response and response.parts:
                    result = response.text
                else:
                    result = "Failed to classify the image."

                st.success(f"Classification Result: {result}")

            except Exception as e:
                st.error(f"Error: {str(e)}")
