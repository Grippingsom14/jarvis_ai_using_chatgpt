import random

replies = {
    "weather": [
        "Initiating atmospheric analysis routines.",
        "Deploying real-time meteorological scanners.",
        "Quantifying current climatic conditions.",
        "Synthesizing the latest meteorological data.",
        "Calibrating for precise weather forecast delivery."
    ],
    "news": [
        "Commencing retrieval of the day's top stories.",
        "Engaging news synthesis protocols.",
        "Aggregating today's significant global events.",
        "Activating current affairs briefing module.",
        "Mining news channels for relevant headlines."
    ],
    "datetime": [
        "Accessing temporal coordinates.",
        "Synchronizing with atomic time standards.",
        "Aligning with Earth's rotation to deduce datetime parameters.",
        "Retrieving standard calendrical metrics.",
        "Updating to the present date and temporal notation."
    ],
    "image_processing": [
        "Activating optical capture mechanisms.",
        "Aligning lenses for high fidelity image acquisition.",
        "Calibrating visual sensors for snapshot.",
        "Preparing image capture protocols.",
        "Optimizing focus parameters for image detail enhancement."
    ]
}


def get_random_integer(min_value=0, max_value=4):
    return random.randint(min_value, max_value)

# Getting a random integer
get_random_integer()

def return_speech_response(speech_for: str):
    return replies[speech_for][get_random_integer()]