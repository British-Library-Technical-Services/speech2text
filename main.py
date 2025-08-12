import os
import glob

from whisper_hf_pipeline import hugging_face_speech2text_pipeline
from whisper_whispertimestamped import whispertimestamped_speech2text_pipeline
from srt_generator_hf import convert_json_to_srt_file

def main():
    MODEL = os.getenv("PT_MODEL_TINY") # tiny model used due to limited hardware capabilities
    AUDIO_LOCATION = os.getenv("AUDIO_LOCATION")
    JSON_OUTPUT = os.getenv("JSON_OUTPUT")
    SRT_OUTPUT = os.getenv("SRT_OUTPUT")

    AUDIO_FILE_LIST = glob.glob(AUDIO_LOCATION + "/*.wav")
    JSON_FILE_LIST = glob.glob(JSON_OUTPUT + "/*.json")

    """Hugging Face Whisper Model for "phrase" level speech transcription"""

    hugging_face_speech2text_pipeline(AUDIO_FILE_LIST, MODEL, JSON_OUTPUT)
    convert_json_to_srt_file(JSON_FILE_LIST, SRT_OUTPUT)

    # whispertimestamped_speech2text_pipeline(AUDIO_FILE_LIST, MODEL, JSON_OUTPUT)

if __name__ == "__main__":
    main()

