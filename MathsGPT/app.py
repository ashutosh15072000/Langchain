import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain,LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool,initialize_agent
from dotenv import load_dotenv
from langchain.callbacks import StreamlitCallbackHandler
load_dotenv()
import os
groq_api_key=os.getenv("GROQ_API_KEY")
## setup up the streamlit app

st.set_page_config(page_title="Text to Math Problem Solver and Data Search Assistant",page_icon="")
st.title("Text to Math Problem Solver Using Google Gemma 2")
groq_api_key=st.sidebar.text_input(label="Groq API KEY",type="password")




if not  groq_api_key:
    st.info("Please add your Groq API KEY to Continue")
    st.stop()


language_model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)


## Initializing the tools
wikipedia_wrapper=WikipediaAPIWrapper()
wikipedia_tools=Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find the various information on the topic ",
)

### Initializa the Math Tool

math_chain=LLMMathChain.from_llm(llm=language_model)
calculator=Tool(
    name="calculator",
    func=math_chain.run,
    description="A tool for math related questions.only input mathematical expression need to be provided"

)

prompt="""
You are a agent tasked for solving users mathematical questions.Logically arrive at the solution and provide a detail explaination and display it point wise for the question below
Question:{question}
Answer:
"""
prompt_template=PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## Combine all the tools into chain
chain=LLMChain(llm=language_model,prompt=prompt_template)

reasoning_tool=Tool(
    name="Reasoning Tool",
    func=chain.run,
    description="A tool for answering logic based and reasoning questions."
)

## initializa the agent

assistant_agent=initialize_agent(
    tools=[wikipedia_tools,calculator,reasoning_tool],
    llm=language_model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in  st.session_state:
    st.session_state['messages']=[
        {"role":"assistant","content":"Hi, I'm Math chatbot who can answer all your maths questions"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])



## Lets start the interaction 
question=st.text_area("Enter your question","I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes.Then I buy a dozen apples and 2 packs of blueberries.Each pack of blueberries contains 25 berries.how many total pieces of fruits do I have at the end?")
if st.button("Find My answer"):
    if question:
        with st.spinner("Generate Response..."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)

            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)

            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb])

            st.session_state.messages.append({"role":"assistant","content":response})
            st.write("Response")
            st.success(response)


    else:
        st.warning("Please Enter Your Input")