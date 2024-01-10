import os
import sys
sys.path.append("misc")
from langchain import hub
from langchain.chains import LLMMathChain
from langchain_openai import OpenAI
from langchain.agents.initialize import initialize_agent
from langchain.agents import Tool
from langchain.agents import AgentType, AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from realtime_data_apis import get_realtime_data
from dotenv import load_dotenv
load_dotenv()
import requests


# os.environ['OPENAI_API_KEY'] = str("xxxxxxxxxxxxxxxxxxxxxxxx")
# os.environ['SERPAPI_API_KEY'] = str("xxxxxxxxxxxxxxxxxxxxxxxx")
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
llm = ChatOpenAI(temperature=1, model="gpt-4-1106-preview", openai_api_key=os.getenv('OPENAI_API_KEY'))


def get_weather(self):
    return get_realtime_data('weather', "")

def get_news(self):
    return get_realtime_data('news', "")


llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

tools = [
    Tool(
        name="Weather",
        func=get_weather,
        description="useful for when you need to answer weather report. You should ask targeted questions"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.invoke,
        description="useful for when you need to answer questions about math"
    ),
    Tool(
        name="News",
        func=get_news,
        description="useful for when you need to answer about latest news headlines."
    )
]
prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_functions_agent(llm, tools, prompt)
openai_agent = AgentExecutor(tools=tools, agent=agent, verbose=True)

result = openai_agent.invoke({"input": "What are the news headlines for today?"})

print(result['output'])
