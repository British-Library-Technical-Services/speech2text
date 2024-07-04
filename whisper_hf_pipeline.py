
from dotenv import load_dotenv
import glob
import torch
from transformers import pipeline
import os
import json
from tqdm import tqdm

MODEL = os.getenv("MODEL_TINY")
AUDIO_LOCATION = os.getenv("AUDIO_LOCATION")
JSON_OUTPUT = os.getenv("JSON_OUTPUT")

FILE_LIST = glob.glob(AUDIO_LOCATION + "/*.wav")

def transcribe_speech(audio_file):
    pipe = pipeline(
        "automatic-speech-recognition", model=MODEL, chunk_length_s=20, device="cpu"
    )

    try:
        prediction = pipe(audio_file, batch_size=8, return_timestamps=True)["chunks"]
        output = json.dumps(prediction, indent=2)
    except Exception as e:
        print(f"Predicton Error: {e}")

    filename = os.path.basename(audio_file).replace(".wav", ".json")

    try:
        with open(os.path.join(JSON_OUTPUT, filename), "w") as f:
            f.write(output)
    except IOError as e:
        print(f"File Write Error: {e}")

for file in tqdm(FILE_LIST, desc="Transcribing Audio Files"):
    transcribe_speech(file)