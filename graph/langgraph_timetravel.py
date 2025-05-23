from fastapi import FastAPI
import os
from typing import Annotated, TypedDict
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
llm = init_chat_model(model="gpt-4o-mini",openai_api_key=openai_api_key)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
graph_builder = StateGraph(State)

tool = TavilySearch(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools",tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

graph_builder.add_edge("tools","chatbot")
graph_builder.add_edge(START,"chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

print(graph,"graph=====")


config = {"configurable": { "thread_id":"1"}}

events = graph.stream(
    {"messages": [{"role":"user","content": "I'm learning LangGraph." "Could you do some research on it for me?"}]},
    config,
    stream_mode='values'
)

for event in events:
    event["messages"][-1].pretty_print()
    
events = graph.stream(
    {"messages": [{"role":"user","content":"Ya thats helpful. Maybe Ill" "build an autonomous agent with it!"}]},
    config,
    stream_mode='values'
)
for event in events:
    event["messages"][-1].pretty_print()
    
to_replay = None
for state in graph.get_state_history(config):
    print("Num Messages: ", len(state.values["messages"]), "Next: ", state.next)
    print("-" * 80)
    if len(state.values["messages"]) == 6:
        # We are somewhat arbitrarily selecting a specific state based on the number of chat messages in the state.
        to_replay = state

print(to_replay.next)
print(to_replay.config)

# The `checkpoint_id` in the `to_replay.config` corresponds to a state we've persisted to our checkpointer.
for event in graph.stream(None, to_replay.config, stream_mode="values"):
    if "messages" in event:
        event["messages"][-1].pretty_print()