# Basic Langgraph including simple Langgraph agent, config functionality and checkpointer(in Memory Saver)

import os
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool
from langgraph.config import get_stream_writer

app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4o-mini",openai_api_key=openai_api_key).with_fallbacks([ChatOpenAI(model="gpt-4o-mini")])

checkpointer = InMemorySaver()

def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:  
    user_name = config["configurable"].get("user_name")
    system_msg = f"You are a helpful assistant. Address the user as {user_name}."
    return [{"role": "system", "content": system_msg}] + state["messages"]

@tool
def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    writer = get_stream_writer()
    writer(f"Looking up data for city: {city}")
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model=model,
    tools=[get_weather],
    # prompt=prompt
    # checkpointer=checkpointer
)

# Run the agent
# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
#     config={"configurable": {"user_name": "John Doe"}}
# )
# print(result,"result=====")

config = {"configurable": {"thread_id": "1"}}
# sf_response = agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
#     config  
# )
# print(sf_response,"sf==========")

# ny_response = agent.invoke(
#     {"messages": [{"role": "user", "content": "what about ny?"}]},
#     config
# )
# print(ny_response,"ny=========")

for stream_mode, chunk in agent.stream(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    stream_mode = ['updates', 'messages', 'custom']
):
    print(chunk)
    print("\n")