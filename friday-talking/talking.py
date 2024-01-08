import pyttsx3

engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 165)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)


def talk(message):
    engine.say(message)
    engine.runAndWait()

    # while True:
    #     try:
    #         engine.runAndWait()
    #         return
    #     except KeyboardInterrupt:
    #         engine.stop()
    #         return
