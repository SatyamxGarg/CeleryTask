import os
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent, Tool
from langchain_core.chat_history import InMemoryChatMessageHistory

app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini",openai_api_key=openai_api_key)
memory = InMemoryChatMessageHistory(session_id="test-session")

def get_capital(country):
    if country.lower() == 'france':
        return "Paris"
    return "Unknown"

def get_weather(city: str) -> str:
        return f"The weather in {city} is sunny."

tools = [
    Tool(name="GetCapital", func = get_capital, description="It adds the value to the input"),
    Tool(name="GetWeather", func = get_weather, description="Gets the weather of city"),
]

query = "what is the capital of France and what's the weather there?"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools,return_intermediate_steps=True)

result = agent_executor.invoke({"input": query})
print(result,"=====")