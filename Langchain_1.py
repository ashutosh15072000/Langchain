import os
from Prompt_templates.constant import openai_key
from langchain.llms import OpenAI
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

## streamlit framemwork

os.environ['OPENAI_API_KEY']=openai_key

st.title("Celebrity Search Result")
input_text=st.text_input("Search The Topic You Want")


## OPENAI LLM MODEL
llms=OpenAI(temperature=0.8)


first_input_prompt=PromptTemplate(
    input_variables=['name'],
    template="Tell About You {name}"
)

second_input_prompt=PromptTemplate(
    input_variables=['person'],
    template="When was {person} born"
)


third_input_prompt=PromptTemplate(
    input_variables=['dob'],
    template="Mention five major event happend arround {dob} in  india"
)


chain=LLMChain(llm=llms,prompt=first_input_prompt,verbose=True,output_key='person')
chain2=LLMChain(llm=llms,prompt=second_input_prompt,verbose=True,output_key='dob')
chain3=LLMChain(llm=llms,prompt=third_input_prompt,verbose=True,output_key='decrption')

from langchain.chains import SimpleSequentialChain
from langchain.chains import SequentialChain

# parent_chain=SimpleSequentialChain(chains=[chain,chain2],verbose=True)
parent_chain_1=SequentialChain(chains=[chain,chain2,chain3],input_variables=['name'],output_variables=['person','dob','decrption'],verbose=True)

if input_text:
    st.write(parent_chain_1({'name':input_text}))