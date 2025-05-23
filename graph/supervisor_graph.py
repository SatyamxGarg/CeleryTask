from fastapi import FastAPI
import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini",openai_api_key=openai_api_key)

def book_hotel(hotel_name: str):
    """Book a hotel"""
    return "Hotel {hotel_name} is booked!"

def flight_book(starting:str, destination:str):
    """Book a flight"""
    return "Flight from {starting} to {destination} is booked!"

hotel_assistant = create_react_agent(
    model = llm,
    tools = [book_hotel],
    prompt = "You are hotel booking assistant",
    name = "hotel_assistant"
)

flight_assistant = create_react_agent(
    model = llm,
    tools = [flight_book],
    prompt = "You are a flight booking assistant",
    name = "flight_assistant"
)

supervisor = create_supervisor(
    model = llm,
    agents = [hotel_assistant,flight_assistant],
    prompt = "You manage a hotel booking assistant and a flight booking assistant. Assign work to them."
).compile()

for chunk in supervisor.stream(
    {"messages": [{"role": "user","content": "Book a flight from NY to California and a TAJ Hotel"}]},
    ):
    print(chunk)
    print("\n")
