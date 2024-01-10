import os
import sys
# sys.path.append("jarvis_ai_using_chatgpt/chatgpt-chat")
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
# from openai import OpenAI
from initiate import training_prompt
load_dotenv()

lang_model = os.getenv('OPENAI_LANGUAGE_MODEL')
# llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), model_name="gpt-4-1106-preview")
llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))
memory = ConversationBufferMemory(memory_key="history", return_messages=True, max_token_limit=50)
# memory.load_memory_variables({})

def chat(message):
    try:
        memory.load_memory_variables({})
        # template_model = f"{training_prompt}" + """
        # Current conversation with Rupam and you:
        # {history}
        #
        # Rupam: {input}
        # Friday: """

        template_model = "{history}{input}"


        chat_prompt = PromptTemplate(input_variables=["history", "input"], template=template_model)

        conversation = ConversationChain(
            prompt=chat_prompt,
            llm=llm,
            verbose=True,
            memory=memory
        )
        reply = conversation.predict(input=f"{message}")
        print("Friday: ", reply)
        return reply
    except Exception as err:
        print('Exception: ', err)


chat(input("ask : "))