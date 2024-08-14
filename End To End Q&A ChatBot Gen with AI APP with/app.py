import streamlit as st 
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_PROJECT']="Q&A ChatBot With Gemini"

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are helpful assistant.Please reponse to user queries"),
        ("user","Question:{question}"),
    ]
)

def generate_response(question, api_key, llm, temperature, max_tokens):
    """
    Generate a response to a user's question using the Gemini AI model.

    Args:
        question (str): The user's question.
        api_key (str): The Gemini API key.
        llm (str): The Google model to use (e.g. 'gemini-1.5-pro-001', 'gemini-1.5-flash-001', etc.).
        temperature (float): The temperature parameter for the model (between 0.0 and 1.0).
        max_tokens (int): The maximum number of tokens in the response (between 50 and 1000).

    Returns:
        str: The generated response.

    Example:
        >>> generate_response("What is the capital of France?", "my_api_key", "gemini-1.5-pro-001", 0.7, 150)
        "The capital of France is Paris."
    """
    model_kwargs = {
        "temperature": temperature,
        "max_output_tokens": max_tokens
    }
    llm = GoogleGenerativeAI(model=llm,
                             google_api_key=api_key,
                             model_kwargs=model_kwargs,
                )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

## title of the App
st.title("Enchanced Q&A chatbot with Gemini")

## sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Gemini API KEY:", type="password")

### Drop down select various Google models
llm = st.sidebar.selectbox("Select a Google Model", ['gemini-1.5-pro-001', 'gemini-1.5-flash-001', 'gemini-1.0-pro-vision-001', 'gemini-pro'])

## Adjust response parameter
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=1000, value=150)

## Main Interface for user Input
st.write("Go ahead and ask any question")

user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please enter a question")