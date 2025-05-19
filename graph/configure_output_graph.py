import os
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

app = FastAPI()

openai_api_key = os.getenv("OPEN_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini",openai_api_key=openai_api_key)

class WeatherResponse(BaseModel):
    conditions: str

def get_weathers(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model = model,
    tools = [get_weathers],
    response_format = WeatherResponse
)

result = agent.invoke(
    {"messages": [{"role":"user", "content":"What is the weather in sf?"}]}
)

print(result["structured_response"],"str.response========")

print(result,"result======")