import streamlit as st
from langchain.schema import AIMessage,HumanMessage,SystemMessage
from langchain.chat_models import ChatOpenAI
import os
from langchain.llms import OpenAI
## streamlit UI

st.set_page_config(page_title='Conversationsal Q&A chatbot')
st.header("Hey,Let chats")

from dotenv import load_dotenv
load_dotenv()
chat=ChatOpenAI(temperature=0.5,openai_api_key=os.getenv('OPENAI_API_KEY'))
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages']=[
            SystemMessage(content="You are a comdedian Ai assistant")
    ]
def get_chatmodel_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
                                            
    answer=chat(st.session_state['flowmessages'])

    st.session_state['flowmessages'].append(AIMessage(content=answer.content))


    return answer.content

input=st.text_input("Input:",key='input')
response=get_chatmodel_response(input)

submit=st.button("click")

if submit:
    st.subheader("The Response is")
    st.write(response)