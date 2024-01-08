import os
from flask import Flask, redirect, url_for, request
import sys
sys.path.append("chatgpt-chat")
sys.path.append("friday-talking")
sys.path.append("jarvis-listening")
from dotenv import load_dotenv
from chat import chat
from talking import talk
from listening import jarvis_listening
load_dotenv()

app = Flask(__name__)


while True:
    try:
        audio_file = jarvis_listening()
        bot_reply = chat(audio_file)
        talk(bot_reply)
        # os.remove(audio_file["path"])
    except Exception as e:
        print("Exception occurred: ", e)
        break


@app.route('/success/<name>')
def do_chat(name):
    reply = chat(name)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
