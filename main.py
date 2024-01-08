import os
import pyttsx3
from flask import Flask, redirect, url_for, request
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
app = Flask(__name__)


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))

def jarvis_talks():
    print('TEST')
    # USERNAME = "Sir"
    # BOTNAME = "JARVIS"
    #
    engine = pyttsx3.init('sapi5')

    # Set Rate
    engine.setProperty('rate', 175)

    # Set Volume
    engine.setProperty('volume', 1.0)

    # Set Voice (Female)
    voices = engine.getProperty('voices')
    print(voices)

    engine.setProperty('voice', voices[1].id)
    engine.say("Sir! There is an emergency in the OT")
    engine.runAndWait()

    # response = client.audio.speech.create(
    #     model="tts-1",
    #     voice="nova",
    #     input="Sir! There is an emergency in the OT",
    # )
    # print(response)
    # response.stream_to_file("output.mp3")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
