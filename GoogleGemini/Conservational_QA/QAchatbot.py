import os
# Import the os module to interact with the operating system
from dotenv import load_dotenv
# Import the load_dotenv function to load environment variables from a .env file
load_dotenv()
# Load environment variables from a .env file

import google.generativeai as genai
# Import the google.generativeai module to interact with the Generative AI API
import streamlit as st
# Import the streamlit module to create a web-based interface for the application

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
# Get the Google API key from the environment variables
genai.configure(api_key=GOOGLE_API_KEY)
# Configure the Generative AI API with the Google API key

model=genai.GenerativeModel("gemini-1.5-pro")
# Create a GenerativeModel instance with the "gemini-1.5-pro" model
chat=model.start_chat(history=[])
# Start a new chat session with the model and an empty history

def get_gemini_response(question):
    # Define a function to get a response from the Gemini model
    response=chat.send_message(question,stream=True)
    # Send a message to the chat session and get a response
    return response
    # Return the response from the model

st.set_page_config(page_title="Q&A Demo",page_icon="🧊", layout="wide")
# Set the page configuration for the Streamlit application

st.header("Gemini LLM Application")
# Display a header with the application title

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
# Initialize the chat history in the session state if it doesn't exist

input=st.text_input("Input:",key="input")
# Create a text input field for the user to enter a question

submit=st.button("Ask the Question")
# Create a button to submit the question

if submit and  input:
    # Check if the submit button is clicked and the input field is not empty
    response=get_gemini_response(input)
    # Get a response from the Gemini model
    st.session_state['chat_history'].append(("You",input))
    # Add the user's question to the chat history
    st.subheader("The Response is")
    # Display a subheader for the response
    for chunk in response:
        st.write(chunk.text)
        # Display the response from the model
        st.session_state['chat_history'].append(("Bot",chunk.text))
        # Add the response to the chat history

with st.sidebar:
    # Create a sidebar for the application
    chat_history_button=st.button("Chat History")
    # Create a button to display the chat history

    if chat_history_button:
        # Check if the chat history button is clicked
        st.subheader("The Chat History is")
        # Display a subheader for the chat history
        for role,text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")
            # Display the chat history