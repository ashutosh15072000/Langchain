
"""
Langchain with LLama3.1 Streamlit App

This app uses the Langchain library to create a conversational AI model using the LLama3.1 model.
It takes a user's question as input and responds with a helpful answer.

Example:
--------

1. Run the app by executing `streamlit run app.py` (assuming this code is in a file named `app.py`)
2. Enter a question in the text input field, e.g. "What is the capital of France?"
3. Press Enter to submit the question
4. The app will display the response from the LLama3.1 model

"""

from langchain_ollama import OllamaLLM
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set Google API key environment variable
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_MODEL_API_KEY")

### Prompt Template

def create_prompt_template():
    """
    Create a chat prompt template for the LLama3.1 model.

    Returns:
        ChatPromptTemplate: A chat prompt template with a system message and a user message.
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Please respond to the question asked"),
            ("user", "Question: {question}")
        ]
    )

prompt = create_prompt_template()

## Streamlit Framework

def create_streamlit_app():
    """
    Create a Streamlit app with a text input field and a button to submit the question.

    Returns:
        None
    """
    st.title("LLama3.1 with Ollama")
    input_text = st.text_input("What question do you have in mind?")
    button=st.button("sumbit")

    ## Ollama Llama3.1 Model

    def create_llama_model():
        """
        Create an instance of the OllamaLLM model with the LLama3.1 model.

        Returns:
            OllamaLLM: An instance of the OllamaLLM model.
        """
        return OllamaLLM(model="llama3.1")

    llm = create_llama_model()

    def create_output_parser():
        """
        Create an instance of the StrOutputParser.

        Returns:
            StrOutputParser: An instance of the StrOutputParser.
        """
        return StrOutputParser()

    output_parser = create_output_parser()

    def create_chain():
        """
        Create a chain of the prompt template, LLama3.1 model, and output parser.

        Returns:
            Chain: A chain of the prompt template, LLama3.1 model, and output parser.
        """
        return prompt | llm | output_parser

    chain = create_chain()
    
    if button:
        st.write(chain.invoke({"question": input_text}))

create_streamlit_app()