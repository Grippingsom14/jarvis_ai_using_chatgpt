import os
import sys
sys.path.append("chatgpt-chat")
from dotenv import load_dotenv
import pyaudio
import wave
import audioop
import time
import random
import string
from openai import OpenAI
import whisper
client = OpenAI()
load_dotenv()

TEMP_LOCATION = os.getenv('TEMP_AUDIO_FILE_LOCATION')
# openai.api_key = os.getenv('OPENAI_API_KEY')


def whisper_transcribe(_path, random_string):
    model = whisper.load_model("base.en")
    result = model.transcribe(_path, fp16=False)
    return result["text"]


# Function to generate a random string of a given length
def generate_random_string(length):
    # Define the set of characters to choose from
    characters = string.ascii_letters + string.digits  # You can add more characters if needed

    # Generate the random string
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


# Function for audio recording and processing
def jarvis_listening():
    transcribed = ''
    # Define audio parameters
    _format = pyaudio.paInt16
    channels = 1
    refresh_rate = 128000
    chunks = 1024
    threshold_volume = 3000  # Adjust this threshold based on your environment
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open an audio stream for recording
    stream = audio.open(format=_format, channels=channels,
                        rate=refresh_rate, input=True,
                        frames_per_buffer=chunks)

    frames = []  # List to store audio frames
    is_recording = False  # Flag to indicate if recording is in progress
    stopwatch_on = False  # Flag to control elapsed time tracking
    start_time_recorded = 0  # Variable to store start time of User not speaking

    print("Recording...")
    random_string = generate_random_string(6)  # Generate a random string for the audio file name

    while True:
        # Read audio data from the stream
        data = stream.read(chunks)
        rms = audioop.rms(data, 2)  # Calculate RMS (Root Mean Square) to determine volume
        # print(rms)

        # Check if audio volume exceeds the threshold for recording
        if rms > threshold_volume:
            start_time_recorded = time.time()
            if not is_recording:
                print("Start recording")
                is_recording = True

            frames.append(data)  # Store audio frames
        else:
            if is_recording:
                frames.append(data)
                if not stopwatch_on:
                    start_time_recorded = time.time()
                    stopwatch_on = True
                elif stopwatch_on:
                    elapsed_time = time.time() - start_time_recorded
                    secs = float("{:.2f}".format(elapsed_time % 60))
                    print("Elapsed time: ", secs)
                    if secs > 1:
                        # Stop recording and save the audio file
                        audio.close(stream)
                        stream.stop_stream()
                        stream.close()
                        audio.terminate()

                        # Save recorded audio frames as a WAV file
                        wf = wave.open(f"{TEMP_LOCATION}recorded_audio_{random_string}.wav", 'wb')
                        wf.setnchannels(channels)
                        wf.setsampwidth(audio.get_sample_size(_format))
                        wf.setframerate(refresh_rate)
                        wf.writeframes(b''.join(frames))
                        wf.close()

                        print("Stop recording")
                        print(f"Recording saved as : recorded_audio_{random_string}.wav")
                        transcribed = whisper_transcribe(f"{TEMP_LOCATION}recorded_audio_{random_string}.wav", random_string)
                        os.remove(f"{TEMP_LOCATION}recorded_audio_{random_string}.wav")
                        break

    return transcribed
    # Restart the listening process after a delay
    # jarvis_listening()
