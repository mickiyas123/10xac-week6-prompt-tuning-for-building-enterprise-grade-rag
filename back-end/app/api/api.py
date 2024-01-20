from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Importing necessary libraries
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
import nest_asyncio
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


# Load OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")


# Define FastAPI app
app = FastAPI()

class Query(BaseModel):
    query_str: str

# Setting up the environment
tgt_sites = ['https://github.com/f/awesome-chatgpt-prompts',
             'https://www.greataiprompts.com/prompts/best-system-prompts-for-chatgpt/',
             'https://stackdiary.com/chatgpt/role-based-prompts/']

def add_documents(loader, instance):
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", ".", ";", ",", " ", ""])
    texts = text_splitter.split_documents(documents)
    instance.add_documents(texts)

# Instantiate OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Instantiate Chroma instance
instance = Chroma(embedding_function=embeddings, persist_directory='PERSIST_DIRECTORY')

# Load documents from the web
loader = WebBaseLoader(tgt_sites)
if loader:
    add_documents(loader, instance)

# Persist the processed instance
instance.persist()
instance = None

# Reload Chroma instance
instance = Chroma(persist_directory='PERSIST_DIRECTORY', embedding_function=embeddings)

# Instantiate RetrievalQA
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=openai_api_key
    ),
    chain_type="stuff",
    retriever=instance.as_retriever()
)
@app.post("/generate_prompt")
async def generate_prompt(query: Query):
    try:
        # Run the query and get the output string
        output_string = qa.run(query.query_str)
        return {"output_string": output_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

