import os
import sys

sys.path.append("misc")
from langchain.chains import LLMMathChain
from langchain.agents import Tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from realtime_data_apis import get_realtime_data
from langchain.memory import ConversationBufferMemory
from langchain.agents.schema import AgentScratchPadChatPromptTemplate
from langchain.prompts import ChatPromptTemplate
from initiate import training_prompt
from dotenv import load_dotenv

load_dotenv()

# os.environ['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'] = str("xxxxxxxxxxxxxxxxxxxxxxxx")
# os.environ['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'] = str("xxxxxxxxxxxxxxxxxxxxxxxx")
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
llm = ChatOpenAI(temperature=1, model="gpt-4-1106-preview",
                 openai_api_key=os.getenv('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'))
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
# llm_chat = ConversationChain(llm=llm, verbose=True)
memory = ConversationBufferMemory(memory_key="history", return_messages=True, max_token_limit=50)

data_memory = ''


def get_weather(self):
    return get_realtime_data('weather', "")


def get_news(self):
    return get_realtime_data('news', "")


def get_date(self):
    # global data_memory
    # print("data_memory", data_memory)
    # if data_memory == '':
    #     data_memory = "loaded"
    #     return get_realtime_data('date')
    # else:
    #     return

    return get_realtime_data('date')


tools = [
    Tool(
        name="Weather",
        func=get_weather,
        description="useful for when you need to answer weather report, sunrise or sunset time, windspeed, weather forcast or any other weather forcast related information."
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    ),
    Tool(
        name="News",
        func=get_news,
        description="useful for when you need to answer about latest news headlines."
    ),
    Tool(
        name="Date",
        func=get_date,
        description="useful for getting the today's date for user query or any other execution"
    ),
    # Tool(
    #     name="Conversation",
    #     func=llm_chat.run,
    #     description="For natural conversation this tool is needed"
    # )
]

# template_model = """
#     {agent_scratchpad}
#     {history}
#     {input}"""
# prompt = PromptTemplate(input_variables=["history", "input", "agent_scratchpad"], template=template_model)

memory.load_memory_variables({})
template_model = """
{agent_scratchpad}

Current conversation with Rupam and you:
{history}

Rupam: {input}
Friday: """
# print(prompt)

template = ChatPromptTemplate.from_messages([
    ("system", f"{training_prompt}" + "This is the history of the chat {history}"),
    ("human", "{user_input} {input}"),
])

messages = template.format_messages(
    user_input="Hey Friday!"
)
print("MESSAGES : ", messages)
prompt_new = AgentScratchPadChatPromptTemplate(input_variables=["history", "input"], messages=messages)

agent = create_openai_functions_agent(llm, tools, prompt_new)
openai_agent = AgentExecutor(
    tools=tools,
    agent=agent,
    verbose=True,
    memory=memory,
    early_stopping="force",
    # max_execution_time=1
)


def agent_chat(message):
    while True:
        memory.clear()
        # result = openai_agent.invoke({"input": message})
        # result = openai_agent.invoke({"input": input("Ask : ")})
        result = openai_agent.invoke({"input": input("Ask : ")})
        print(result['output'])
        # return result['output']

# https://python.langchain.com/docs/modules/agents/how_to/custom_agent
# https://api.python.langchain.com/en/latest/agents/langchain.agents.schema.AgentScratchPadChatPromptTemplate.html#
# agent_chat("")
