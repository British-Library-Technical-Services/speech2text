
from dotenv import load_dotenv
import glob
import torch
from transformers import pipeline
import os
import json

MODEL = os.getenv("MODEL_TINY")
AUDIO_LOCATION = os.getenv("AUDIO_LOCATION")
JSON_OUTPUT = os.getenv("JSON_OUTPUT")

FILE_LIST = glob.glob(AUDIO_LOCATION + "/*.wav")

def transcribe_speech(audio_file):
    pipe = pipeline(
        "automatic-speech-recognition", model=MODEL, chunk_length_s=20, device="cpu"
    )

    prediction = pipe(audio_file, batch_size=8, return_timestamps=True)["chunks"]
    output = json.dumps(prediction, indent=2)

    filename = os.path.basename(audio_file).replace(".wav", ".json")

    with open(os.path.join(JSON_OUTPUT, filename), "w") as f:
        f.write(output)

for file in FILE_LIST:
    transcribe_speech(file)