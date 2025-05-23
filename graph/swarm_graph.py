from fastapi import FastAPI
import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_swarm, create_handoff_tool


app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini",openai_api_key=openai_api_key)


def book_hotel(hotel_name: str):
    "Book a hotel"
    return "Hotel {hotel_name} is booked!"

def book_flight(starting:str, destination:str):
    "Book a flight"
    return "Flight from {starting} to {destination} is booked!"

transfer_to_hotel = create_handoff_tool(
    agent_name = "hotel_assistant",
    description = "Transfer to hotel assistant"
)

transfer_to_flight = create_handoff_tool(
    agent_name = "flight_assistant",
    description = "Transfer to flight assistant"
)

hotel_assistant = create_react_agent(
    model = llm,
    tools = [book_hotel, transfer_to_flight],
    prompt = "You are hotel booking assistant",
    name = "hotel_assistant"
)

flight_assistant = create_react_agent(
    model = llm,
    tools = [book_flight, transfer_to_hotel],
    prompt = "You are a flight booking assistant",
    name = "flight_assistant"
)

swarm = create_swarm(
    agents = [hotel_assistant, flight_assistant],
    default_active_agent = "flight_assistant"
).compile()

for chunk in swarm.stream(
    {"messages": [{"role": "user","content": "Book a flight from NY to California and a TAJ Hotel"}]},
):
    print(chunk)
    print("\n")