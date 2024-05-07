from langchain.llms import openai

openai_api_key='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'

llm=openai(openai_api_key)
print(llm.invoke("tell me the capital of india"))