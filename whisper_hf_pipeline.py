from transformers import pipeline
import os
import json
from tqdm import tqdm

def transcribe_speech(audio_file, MODEL, JSON_OUTPUT):
    pipe = pipeline(
        "automatic-speech-recognition", model=MODEL, chunk_length_s=20, device="cpu", 
    )

    output = None  # Initialize output
    try:
        prediction = pipe(audio_file, batch_size=8, return_timestamps=True)["chunks"]
        output = json.dumps(prediction, indent=2)
    except Exception as e:
        print(f"Prediction Error: {e}")
        return  # Return early if prediction fails

    filename = os.path.basename(audio_file).replace(".wav", "")

    try:
        with open(os.path.join(JSON_OUTPUT, filename) + "_hfpipeline.json", "w") as f:
            f.write(output)
    except IOError as e:
        print(f"File Write Error: {e}")

def hugging_face_speech2text_pipeline(FILE_LIST, MODEL, JSON_OUTPUT):
    for file in tqdm(FILE_LIST, desc="Transcribing Audio Files"):
        transcribe_speech(file, MODEL, JSON_OUTPUT)