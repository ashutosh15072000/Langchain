import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv
load_dotenv()

def load_groq_api_key() -> str:
    
    # Load the GROQ API key from environment variables.

    # Returns:
    #     str: The GROQ API key.

    # Example:
    #     >>> load_groq_api_key()
    #     'your_groq_api_key_here'
    
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
    return os.getenv('GROQ_API_KEY')

def create_llm(groq_api_key: str) -> ChatGroq:
    
    # Create a LangChain GROQ model instance.

    # Args:
    #     groq_api_key (str): The GROQ API key.

    # Returns:
    #     ChatGroq: The LangChain GROQ model instance.

    # Example:
    #     >>> groq_api_key = load_groq_api_key()
    #     >>> llm = create_llm(groq_api_key)
    
    return ChatGroq(groq_api_key=groq_api_key)

def create_prompt_template() -> ChatPromptTemplate:
    # """
    # Create a LangChain chat prompt template.

    # Returns:
    #     ChatPromptTemplate: The chat prompt template.

    # Example:
    #     >>> prompt = create_prompt_template()
    # """
    return ChatPromptTemplate.from_template(
        """
        Answer the question based on the provided context only.
        Please provide the most accurate response based on the question
        <context>
        {context}
        <context>
        Question:<input>
        """
    )

def create_vector_embeddings() -> None:
    
    # Create vector embeddings for the documents.

    # This function creates the following:
    # - Ollama embeddings model
    # - PyPDF directory loader
    # - Recursive character text splitter
    # - FAISS vector store

    # The vector embeddings are stored in the Streamlit session state.

    # Example:
    #     >>> create_vector_embeddings()
    
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OllamaEmbeddings(model="llama3.1")
        st.session_state.loader = PyPDFDirectoryLoader("data")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

def main() -> None:
  
    # The main function for the Streamlit app.

    # This function creates the LangChain GROQ model, prompt template, and vector embeddings.
    # It then creates a Streamlit text input for the user to enter a query.
    # When the user clicks the 'Document Embeddings' button, it creates the vector embeddings.
    # When the user enters a query, it uses the LangChain model to retrieve relevant documents and displays the results.

    # Example:
    #     >>> main()

    groq_api_key = load_groq_api_key()
    llm = create_llm(groq_api_key)
    prompt = create_prompt_template()

    user_input = st.text_input("Enter the Query from Research paper")

    if st.button("Document Embeddings"):
        create_vector_embeddings()
        st.write("Vector Database is Ready")

    if user_input:
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = st.session_state.vectors.as_retriever()
        retriever_chain = create_retrieval_chain(retriever, document_chain)

        response = retriever_chain.invoke({"input": user_input})

        st.write(response['answer'])

        with st.expander("Document Similarity Search"):
            for i, doc in enumerate(response['context']):
                st.write(doc.page_content)
                st.write("-------------------------------------")

if __name__ == "__main__":
    main()