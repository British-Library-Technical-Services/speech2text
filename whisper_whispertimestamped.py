import os
import whisper_timestamped as whisper
import glob
import json

MODEL = os.getenv("PT_MODEL_TINY")
AUDIO_LOCATION = os.getenv("AUDIO_LOCATION")
JSON_OUTPUT = os.getenv("JSON_OUTPUT")

FILE_LIST = glob.glob(AUDIO_LOCATION + "/*.wav")

def transcribe_speech(audio_file):
    load_model = whisper.load_model(MODEL)
    load_audio = whisper.load_audio(audio_file)

    try:
        transcribe = whisper.transcribe(load_model, load_audio, language="en")
        output = json.dumps(transcribe, indent=2)
    except Exception as e:
        print(f"Prediction Error: {e}")
    
    filename = os.path.basename(audio_file).replace(".wav", "")

    try:
        with open(os.path.join(JSON_OUTPUT, filename) + "_timestamped.json", "w") as f:
            f.write(output)
    except IOError as e:
        print(f"File Write Error: {e}")

for file in FILE_LIST:
    transcribe_speech(file)