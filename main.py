from fastapi import FastAPI
from pydantic import BaseModel
from tasks import generate_answer_task
import os
import json

app = FastAPI()


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask_question(question: Question):
    task = generate_answer_task.delay(question.question)
    return {"task_id": task.id}


# @app.get("/result/{task_id}")
# def get_result(task_id: str):
#     result_path = f"results/{task_id}/result.json"
#     if os.path.exists(result_path):
#         with open(result_path, "r") as f:
#             data = json.load(f)
#         return {"status": "completed", "data": data}
#     return {"status": "processing"}



@app.get("/result/{task_id}")
def get_result(task_id: str):
    folder_path = f"results/{task_id}"

    if not os.path.exists(folder_path):
        return {"status": "processing"}

    results = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            model_name = filename.replace(".json", "")
            with open(os.path.join(folder_path, filename), "r") as f:
                content = json.load(f)
                results.append({
                    "model": model_name,
                    "question": content.get("question"),
                    "answer": content.get("answer")
                })

    return {
        "status": "completed",
        "results": results
    }