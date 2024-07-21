from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
from langserve import add_routes

groq_api = os.getenv('groq_api')
model = ChatGroq(model="Gemma2-9b-It", groq_api_key = groq_api)

#create prompt template
sys_template = "Translate the following into : {language}"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', sys_template),
    ('user', '{text}')
])

parser = StrOutputParser()

#chain
chain = prompt_template|model|parser

#App definition
app = FastAPI(
    title="Language Translator",
    version="1.0",
    description= "Simple Language Translator using Langchain runnable interfaces and Fast API Server"
)

#Adding Routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)