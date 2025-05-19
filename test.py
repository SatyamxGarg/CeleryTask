import os
from fastapi import FastAPI
import openai
from pydantic import BaseModel

app = FastAPI()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

class UserQuestion(BaseModel):
    question: str


def get_openai_answer(question: str) -> str:
    messages = [{"role":"system", "content":"You are an helpful assistant"}]
    messages.append({"role":"user", "content":question})
    response = openai.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages
    )
    answer = response.choices[0].message.content.strip()
    return answer

@app.post("/ask")
def ask_question(question: UserQuestion):
        
    answer = get_openai_answer(question.question)
    print(answer)
    
    return {"status":"Success", "data": answer}
