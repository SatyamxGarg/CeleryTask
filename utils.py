import os
import json
import openai
import httpx
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def fetch_tavily_data(query: str) -> str:
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    payload = {
        "query": query,
        "search_depth": "basic",
        "include_answer": True
    }
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("answer", "")


def generate_gpt_response(question: str, context: str, model: str) -> str:
    openai.api_key = OPENAI_API_KEY
    messages = [
        {"role": "system", "content": f"Use this context to answer: {context}"},
        {"role": "user", "content": question}
    ]
    response = openai.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content.strip()


# def save_result(task_id: str, result: dict):
#     folder_path = f"results/{task_id}"
#     os.makedirs(folder_path, exist_ok=True)
#     with open(f"{folder_path}/result.json", "w") as f:
#         json.dump(result, f, indent=2)


