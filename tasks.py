import json
from celery import chord, shared_task, group
import os
from utils import fetch_tavily_data, generate_gpt_response
from celery_worker import celery_app


@celery_app.task(name="tasks.generate_answer_task")
def generate_answer_task(question: str):
    tavily_data = fetch_tavily_data(question)
    task_id = generate_answer_task.request.id

    child1 = generate_child_response.s(question, tavily_data, "gpt-4o-mini")
    child2 = generate_child_response.s(question, tavily_data, "gpt-3.5-turbo")
    return chord([child1, child2])(save_result.s(question,task_id))


@celery_app.task(name="tasks.generate_child_response")
def generate_child_response(question: str, context: str, model: str):
     answer = generate_gpt_response(question, context, model)
     return {"model": model, "question": question, "answer": answer}



# @celery_app.task(name="tasks.save_result")
# def save_result(results, question):
#     final_result = {
#         "question": question,
#         "answers": results
#     }

#     # Generate a unique ID to save result
#     from celery import current_task
#     task_id = current_task.request.id

#     folder_path = f"results/{task_id}"
#     os.makedirs(folder_path, exist_ok=True)
#     with open(f"{folder_path}/result.json", "w") as f:
#         json.dump(final_result, f, indent=2)

#     return final_result

@celery_app.task(name="tasks.save_result")
def save_result(results, question, parent_task_id):
    folder_path = f"results/{parent_task_id}"
    os.makedirs(folder_path, exist_ok=True)

    for result in results:
        model = result["model"]
        file_path = os.path.join(folder_path, f"{model}.json")
        with open(file_path, "w") as f:
            json.dump({
                "question": result["question"],
                "answer": result["answer"]
            }, f, indent=2)

    return {"status": "saved", "folder": folder_path}
