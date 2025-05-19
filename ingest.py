from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile, Form
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from models import add_source, remove_source
from chromaDB import get_vetor_store
from langchain.docstore.document import Document

app = FastAPI()

load_dotenv()

class DeletePDFRequest(BaseModel):
    user_id: int
    user_name: str
    pdf_id: int


@app.post("/ingest")
async def upload_pdf(user_id: str = Form(...),user_name: str = Form(...), file: UploadFile = File(...)):
    pdf_file_path = f"/tmp/{file.filename}"
    with open(pdf_file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    loader = PyPDFLoader(file_path=pdf_file_path)
    text = ""
    async for page in loader.alazy_load():
        text += page.page_content
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    
    docs = []
    
    for chunk in chunks:
        docs.append(Document(page_content=chunk, metadata={'name':file.filename}))
    
    vec_store = get_vetor_store(collection_name=str(user_id+user_name))
    ids = await vec_store.aadd_documents(docs)
    
    add_source(user_id,file.filename,ids)
    
    
    return {"message": "PDF uploaded", "pdf_id": ids, "user_id": user_id}


@app.post("/expel")
async def expel_pdf(delete_request: DeletePDFRequest):
    user_id = delete_request.user_id
    user_name = delete_request.user_name
    user_pdf_id = delete_request.pdf_id
    
    vec_store_del = get_vetor_store(collection_name=str(user_id) + user_name)
    
    try:
        pdf_ids = remove_source(user_id, user_pdf_id)
        await vec_store_del.adelete(ids=pdf_ids)

        return {"message": "PDF successfully removed", 'status':True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured: {str(e)}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)