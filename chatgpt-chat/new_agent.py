import sys
sys.path.append("misc")
sys.path.append("friday-talking")
import json
from typing import Sequence, List
from llama_index.llms import OpenAI, ChatMessage
from llama_index.tools import BaseTool, FunctionTool
from initiate import training_prompt
from custom_replies import return_speech_response
from describe_image import describe_image
from process_exec import exec_process
from realtime_data_apis import get_realtime_data
import nest_asyncio
from talking import talk

nest_asyncio.apply()


def get_datetime() -> str:
    """get the today's date, current time and returns the datetime string"""
    talk(return_speech_response("datetime"))
    return get_realtime_data('datetime')


def get_news() -> dict:
    """get news for today's latest headlines and returns the news data as a dictionary"""
    talk(return_speech_response("news"))
    return get_realtime_data('news')


def get_weather(location: str = "") -> dict:
    """get the current weather forecast, sunrise time, sunset time, wind speed,
    wind direction etc. and returns the weather data as a dictionary"""
    talk(return_speech_response("weather"))
    return get_realtime_data('weather')


def capture_image_and_get_description(query_for_the_image: str = "") -> str:
    print("query: ", query_for_the_image)
    """You can see using camera and take a picture and get the description of the captured image.
    Variable 'query_for_the_image' holds the query for which user is asking in the camera and this method returns the 
    captured image description as a string"""
    talk(return_speech_response("image_processing"))
    return describe_image()


def execute_command(command: str) -> str:
    """get the description of the image and returns the string"""
    return exec_process()


# multiply_tool = FunctionTool.from_defaults(fn=multiply)
# add_tool = FunctionTool.from_defaults(fn=add)
datetime_tool = FunctionTool.from_defaults(fn=get_datetime)
weather_tool = FunctionTool.from_defaults(fn=get_weather)
news_tool = FunctionTool.from_defaults(fn=get_news)
capture_image_tool = FunctionTool.from_defaults(fn=capture_image_and_get_description)


class AgentFriday:
    def __init__(
            self,
            tools: Sequence[BaseTool] = [],
            llm: OpenAI = OpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
            chat_history: List[ChatMessage] = [],
            default_template: str = training_prompt
    ) -> None:
        self._llm = llm
        self._tools = {tool.metadata.name: tool for tool in tools}
        self._chat_history = chat_history
        self._default_template = default_template

    def reset(self) -> None:
        self._chat_history = []

    def chat(self, message: str) -> str:
        chat_history = [ChatMessage(role="system", content=self._default_template)] + self._chat_history
        chat_history.append(ChatMessage(role="user", content=message))
        tools = [
            tool.metadata.to_openai_tool() for _, tool in self._tools.items()
        ]

        ai_message = self._llm.chat(chat_history, tools=tools).message
        additional_kwargs = ai_message.additional_kwargs
        chat_history.append(ai_message)

        tool_calls = ai_message.additional_kwargs.get("tool_calls", None)
        # parallel function calling is now supported
        if tool_calls is not None:
            for tool_call in tool_calls:
                function_message = self._call_function(tool_call)
                chat_history.append(function_message)
                ai_message = self._llm.chat(chat_history).message
                chat_history.append(ai_message)

        return ai_message.content

    def _call_function(self, tool_call) -> ChatMessage:
        id_ = tool_call.id
        function_call = tool_call.function
        print("Fn Call ---------------", function_call, "\n\n")
        tool = self._tools[function_call.name]
        output = tool(**json.loads(function_call.arguments))

        return ChatMessage(
            name=function_call.name,
            content=str(output),
            role="tool",
            additional_kwargs={
                "tool_call_id": id_,
                "name": function_call.name,
            },
        )


# while True:
#     print(agent.chat(input("Ask: ")))


def chat_with_agent(message):
    agent = AgentFriday(tools=[news_tool, datetime_tool, weather_tool, capture_image_tool])
    reply = agent.chat(message)
    print(reply)
    return reply
