import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.docstore.document import Document


# data = [
#     Document(page_content="this is", metadata={'name':'pdf name'}),
#     Document(page_content="the testing", metadata={'name':'pdf name'}),
#     Document(page_content="of", metadata={'name':'pdf name'}),
#     Document(page_content="afasfa", metadata={'name':'pdf name'}),
#     Document(page_content="afasfa", metadata={'name':'pdf name'}),
#     Document(page_content="afasfa", metadata={'name':'pdf name'}),
#     Document(page_content="afasfa", metadata={'name':'pdf name'}),
# ]

app = FastAPI()

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini", openai_api_key = openai_api_key)
@app.get("/test-pdf")
async def func():
    loader = PyPDFLoader(file_path="/var/www/html/Example_pdf2.pdf")
    pages = []
    
    async for page in loader.alazy_load():
        pages.append(page)
    vector_store = InMemoryVectorStore.from_documents(pages, OpenAIEmbeddings())
    
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 1})

    retrieved_docs = retriever.invoke("Which countries are mentioned here?")

    print(len(retrieved_docs))
    print(retrieved_docs[0])
  
    return {
        "doc_count": len(retrieved_docs),
        "first_doc": retrieved_docs[0].page_content if retrieved_docs else "No docs found"
    }
  