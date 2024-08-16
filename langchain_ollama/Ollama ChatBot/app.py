from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_ollama.llms import OllamaLLM

## Langsmith Tracking
os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_PROJECT']="Simple Q&A Chatbot With OLLAMA"

### Prompt

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful.Please reponse to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_reponse(question, engine, temperature, max_tokens):
    """
    Generate a response to a user's question using the Ollama LLM.

    Args:
        question (str): The user's question.
        engine (str): The name of the Ollama model to use (e.g. 'llama3.1', 'phi3', 'gemma2').
        temperature (float): The temperature parameter for the LLM (between 0.0 and 1.0).
        max_tokens (int): The maximum number of tokens to generate in the response.

    Returns:
        str: The generated response.

    Example:
        >>> generate_reponse("What is the capital of France?", "llama3.1", 0.7, 150)
        "The capital of France is Paris."
    """
    llm=OllamaLLM(model=engine,temperature=temperature,num_predict=max_tokens)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({"question":question})
    return answer

## title of the App
st.title("Enchanced Q&A chatbot with Ollama")

## sidebar for settings
st.sidebar.title("Settings")

### Drop down select various Google models
engine = st.sidebar.selectbox("Select a Open Source  Model", ['llama3.1', 'phi3', "gemma2"])

## Adjust response parameter
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=1000, value=150)

## Main Interface for user Input
st.write("Go ahead and ask any question")

user_input = st.text_input("You:")

if user_input:
    response = generate_reponse(user_input, engine, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please enter a question")