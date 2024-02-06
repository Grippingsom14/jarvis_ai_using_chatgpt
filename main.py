import os
from flask import Flask, redirect, url_for, request
import sys
sys.path.append("chatgpt-chat")
sys.path.append("friday-talking")
sys.path.append("jarvis-listening")
from dotenv import load_dotenv
from AIChat import chat
from talking import talk
from listening import jarvis_listening
from agentpy import chat_with_agent
load_dotenv()

app = Flask(__name__)


while True:
    try:
        audio_file_transcribed = jarvis_listening()
        bot_reply = chat_with_agent(audio_file_transcribed)
        talk(bot_reply)
        #os.remove(audio_file["path"])
    except Exception as e:
        print("Exception occurred: ", e)
        talk("")
        break


if __name__ == '__main__':
    app.run(debug=True, port=5000)
