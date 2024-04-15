## Q&A chatbot

from langchain.llms import OpenAI

from dotenv import load_dotenv

import streamlit as st

import os

load_dotenv()

## fucntion to load openai model and get response


def get_openai_response(question):
    llm=OpenAI(model_name='gpt-3.5-turbo-instruct',temperature=0.5,openai_api_key=os.getenv('OPENAI_API_KEY'))
    response=llm(question)
    return response

## initalize our streamlit

st.set_page_config(page_title="Q&A Demo")
st.header("Langchain Application")
input=st.text_input("Input: ",key='input')
submit=st.button("Ask the Question")


response=get_openai_response(input)

    ## if ask button is clicked

if submit:
    st.subheader("The Response is")
    st.write(response)