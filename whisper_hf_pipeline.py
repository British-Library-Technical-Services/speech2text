from typing import List, TextIO
from transformers import pipeline
import os
import json


def transcribe_speech(audio_file: str, asr_model: str, json_output: str) -> str:
    pipe = pipeline(
        "automatic-speech-recognition",
        model=asr_model,
        chunk_length_s=20,
        device="cpu",
        ignore_warning=True,
    )

    transcription: str = None
    try:
        prediction = pipe(audio_file, batch_size=8, return_timestamps=True)["chunks"]
        if not prediction:
            print(f"No output generated for {audio_file}")
            return None

        transcription = json.dumps(prediction, indent=2)
        return transcription

    except Exception as e:
        raise Exception(
            f"Error generating speech to text output for {audio_file}: {str(e)}"
        )


def write_transcript_json_file(
    transcription: str, audio_file: str, json_output: str
) -> None:
    generated_json_transcript: TextIO = None
    filename = os.path.basename(audio_file).replace(".wav", ".json")
    try:
        with open(
            os.path.join(json_output, filename), "w", encoding="utf-8"
        ) as generated_json_transcript:
            generated_json_transcript.write(transcription)
            return generated_json_transcript

    except OSError as ose:
        raise OSError(f"Error writing transcription file for {audio_file}: {str(ose)}")
