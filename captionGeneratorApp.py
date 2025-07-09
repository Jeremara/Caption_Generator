import requests
from PIL import Image
import streamlit as st

# Define the APIs of captioning and instruct Models
API_URL_Semantics = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
API_URL_caption = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"


headers = {"Authorization": "Bearer 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"}

# Function to create semantics
def generate_semantics(file):
    response = requests.post(API_URL_Semantics, headers=headers, data=file)
    return response.json()[0]["generated_text"]

# Function to create caption
def generate_caption(payload):
    response = requests.post(API_URL_caption, headers=headers, json=payload)
    return response.json()[0]["generated_text"]

# Function to create HTML markup for favicon and text
def display_image(image_path, width=100):
    image = Image.open(image_path)
    st.image(image, width=width, use_container_width=False)


# set image as navbar
st.image('images/Caption_Generator.png', use_container_width=True)


# Define paths to the PNG images and text
facebook_image_path = "images/facebook.png"
whatApps_image_path = "images/whatsapp.png"
instagram_image_path = "images/instagram.png"
twitter_image_path = "images/twitter.png"


# Display images horizontally
st.write("<h3 style='text-align: center;'>Get the Best Caption to Spark your Image on the following Social Media "
         "Platform</h3>", unsafe_allow_html=True)
st.image([facebook_image_path, whatApps_image_path, instagram_image_path, twitter_image_path],
         width=50, use_container_width=False)

# creating a upload section for users
file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

# checking and splitting the image and caption into section
if file:
    col1, col2 = st.columns(2)
    with col1:
        st.image(file, use_container_width=True)
    with col2:
        with st.spinner("Generating Semantics....."):
            semantics = generate_semantics(file)

        with st.spinner("Generating Caption......"):
            prompt_dic = {"inputs": f"Question:Convert the following image semantics"
                                    f"'{semantics}' to an social media caption "
                                    f"make sure to add hash tags and emojis."
                                    f"Answer: "}
            caption_raw = generate_caption(prompt_dic)
            st.subheader("Caption")

            caption = caption_raw.split("Answer: ")[1]
            
            # Define CSS style for the text box
            text_style = """
                background-color: #f4f4f4;
                padding: 20px;
                border: 2px solid #ddd;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                color: #000;
            """

            # Apply the style to the text box and display the dynamic text
            st.write(
                f'<div style="{text_style}">'
                f'<p>{caption}</p>'
                f'</div>',
                unsafe_allow_html=True
            )



