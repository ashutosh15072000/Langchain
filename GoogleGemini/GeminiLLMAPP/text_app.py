from dotenv import load_dotenv  # Importing the load_dotenv function to load environment variables
import os  # Importing the OS module to interact with the operating system
load_dotenv()  # Loading the environment variables

import streamlit as st  # Importing the Streamlit library for creating web applications
import google.generativeai as genai  # Importing the Google Generative AI library for AI models

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")  # Getting the Google API key from the environment variables

# Configuring the Google Generative AI library with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Defining a function to get a response from the Gemini model
def get_gemini_response(question):
    # Creating an instance of the Gemini model
    model=genai.GenerativeModel("gemini-pro")
    
    # Generating content using the Gemini model
    response=model.generate_content(question)

    # Returning the text response
    return response.text

# Setting the page configuration for the Streamlit application
st.set_page_config(page_title="Q&A Demo")

# Adding a header to the application
st.header("Gemini LLM Application 🎯🌎")

# Creating a text input field for the user to input their question
input=st.text_input("Input",key="input")

# Creating a button to submit the question
submit=st.button("Ask the question 💪🏻")

# Checking if the submit button is clicked
if submit:
    # Getting the response from the Gemini model
    response=get_gemini_response(input)
    
    # Displaying the response
    st.write("Gemini's Response:👌🏻")
    st.write(response)