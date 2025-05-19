from langchain_community.vectorstores.chroma import Chroma 
from langchain_openai.embeddings.base import OpenAIEmbeddings

def get_vetor_store(collection_name:str = '') -> Chroma:
    client = Chroma(
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddings(),
        persist_directory='./chroma',
        )
    return client