import os
import whisper_timestamped as whisper
import json

def transcribe_speech(audio_file, MODEL, JSON_OUTPUT):
    load_model = whisper.load_model(MODEL)
    load_audio = whisper.load_audio(audio_file)

    output = None  # Initialize output
    try:
        transcribe = whisper.transcribe(load_model, load_audio, language="en")
        output = json.dumps(transcribe, indent=2)
    except Exception as e:
        print(f"Prediction Error: {e}")
        return  # Return early if transcription fails
    
    filename = os.path.basename(audio_file).replace(".wav", "")

    try:
        with open(os.path.join(JSON_OUTPUT, filename) + "_timestamped.json", "w") as f:
            f.write(output)
    except IOError as e:
        print(f"File Write Error: {e}")

def whispertimestamped_speech2text_pipeline(FILE_LIST, MODEL, JSON_OUTPUT):
    for file in FILE_LIST:
        transcribe_speech(file, MODEL, JSON_OUTPUT)