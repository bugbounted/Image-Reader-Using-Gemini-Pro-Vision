from dotenv import load_dotenv

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#function to load gemini pro

model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploader_file):
    if uploader_file is not None:
        bytes_data = uploader_file.getvalue()

        image_parts=[
            {
                "mime_type" : uploader_file.type,
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file Uploaded")
# initialize streamlit app

st.set_page_config(page_title="Image Invoice Extractor")

st.header("Image Reader using Gemini Vision Pro")
input = st.text_input("Input Prompt : ",key = "input")
uploader_file = st.file_uploader("Choose an image",type=["jpg","jpeg","png"])
image=''

if uploader_file is not None:
    image = Image.open(uploader_file)
    st.image(image,caption = "Upload Image",use_column_width=True)

submit=st.button("Tell information in image")
input_prompt = """
ask any information in the image and it will retrivel from image
"""

#if button is clicked
if submit:
    image_data = input_image_setup(uploader_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(response)