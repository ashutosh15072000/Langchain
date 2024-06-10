# Q&A Chatbot

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()  # take environment variables from.env.

# Set API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

## Function to load OpenAI model and get responses
def get_gemini_response(input,image):
    model = genai.GenerativeModel('models/gemini-pro-vision')
    if input!= "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

## Initialize our Streamlit app
st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")

input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image =""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

## If ask button is clicked
if submit:
    try:
        response = get_gemini_response(input, image)
        st.subheader("The Response is")
        st.markdown(f"```{response}```")  # Format response as a code block
    except Exception as e:
        st.error(f"Error: {e}")

st.stop()  # Ensure the app is properly shut down