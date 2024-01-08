import os
import sys
# sys.path.append("jarvis_ai_using_chatgpt/chatgpt-chat")
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
# from openai import OpenAI
from initiate import training_prompt
load_dotenv()
# from openai import OpenAI
# client = OpenAI()
# openai.api_key = os.getenv("OPENAI_API_KEY")

lang_model = os.getenv('OPENAI_LANGUAGE_MODEL')
# llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), model_name="gpt-4")
llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))

# memory.load_memory_variables({})

def chat(message):
    template_model = f"{training_prompt}" + """
    Current conversation with Rupam and you:
    {history}
    
    Rupam: {input}
    Friday: """

    memory = ConversationBufferMemory(memory_key="history")

    chat_prompt = PromptTemplate(input_variables=["history", "input"], template=template_model)

    conversation = ConversationChain(
        prompt=chat_prompt,
        llm=llm,
        verbose=True,
        memory=memory
    )
    reply = conversation.predict(input=f"{message}")
    return reply

    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Who won the world series in 2020?"},
    #         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #         {"role": "user", "content": "Where was it played?"}
    #     ]
    # )



# chat('hello')