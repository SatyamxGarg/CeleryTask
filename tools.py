from fastapi import FastAPI
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os
from pydantic import BaseModel, EmailStr, Field
from langchain_core.messages import HumanMessage

app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")


@tool
def multiply(a: int, b: int) -> int:
    """ Multiply a and b"""
    return a*b

@tool
def addition(a: int, b:int) -> int:
    """" Add a and b"""
    return a+b

# class multiply(BaseModel):
#     a: int = Field(..., description="integer a value")
#     b: int = Field(..., description="integer b value")
    
# class addition(BaseModel):
#     a: int = Field(..., description="integer a value")
#     b: int = Field(..., description="integer b value")
    
    
tools=[multiply, addition]

llm = ChatOpenAI(model="gpt-4")
tool_choice="auto"
llm_with_tools = llm.bind_tools(tools)


query = "What is 3 * 12? Also, what is 11 + 49?"

messages = [HumanMessage(query)]

result = llm_with_tools.invoke(messages)

print(result.tool_calls,"result====")

messages.append(result)

for tool_call in result.tool_calls:
    selected_tool = {"add": addition, "multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

print(messages,"message=====")

print(llm_with_tools.invoke(messages))
