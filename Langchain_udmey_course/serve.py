from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langserve import add_routes

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

### Prompt Templates
from langchain_core.prompts import ChatPromptTemplate
generic_template = "Translate the following into {language}:"

"""
ChatPromptTemplate is used to define a prompt template for the language model.
In this case, we're using a generic template that takes two inputs: 
- system: a string that specifies the language to translate to
- user: the text to be translated
"""
prompt_template = ChatPromptTemplate(
    [("system", generic_template), ("user", "{text}")]
)

"""
StrOutputParser is used to parse the output of the language model into a string.
"""
parser = StrOutputParser()

"""
The chain is defined by piping the prompt template to the language model and then to the output parser.
"""
chain = prompt_template | llm | parser

## App definition
"""
FastAPI app definition
"""
app = FastAPI(title="Langchain Serve", version="1.0", description="A simple Api Server using Langchain runnable interfaces")

## Adding chain routes
"""
Add routes to the app for the chain
"""
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    """
    Run the app using uvicorn
    """
    uvicorn.run(app, host="127.0.0.1", port=8000)

"""
Example usage:

curl -X POST \
  http://127.0.0.1:8000/chain \
  -H 'Content-Type: application/json' \
  -d '{"language": "es", "text": "Hello, world!"}'

Response:
"¡Hola, mundo!"
"""