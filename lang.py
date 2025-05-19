from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langserve import add_routes

model = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()

# messages = [
#     SystemMessage(content="Translate the following from English into Italian"),
#     HumanMessage(content="I m fine"),
#     HumanMessage(content="How are you?"),
# ]

# result = model.invoke(messages)
# print(result,"result====")

# print(parser.invoke(result),"=====in invoke")

# chain = model | parser
# print(chain.invoke(messages),"chaining========")

#Prompt Example
system_template = "Translate the following into {language}:"

prompt_template = ChatPromptTemplate.from_messages(
    [("system",system_template),("user","{text}")]
)

result = prompt_template.invoke({"language":"Italian","text":"Hello"})
print(result.to_messages())


# response = model.invoke(result)
# print(response.content)

chain = prompt_template | model | parser
print(chain.invoke({"language":"Hindi","text":"Message is converted."}))


app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

add_routes(
    app,
    chain,
    # model | parser,
    path="/chain",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)