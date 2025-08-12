"""
Speech-to-Text Processing Pipeline

This module provides the main entry point for a speech-to-text processing pipeline
and generates SRT subtitle files.

The pipeline supports two transcription methods:
1. Hugging Face Transformers pipeline (default, phrase level timestamps)
2. Whisper Timestamped (word level timestamps)

Environment Variables Required:
    PT_MODEL_TINY: Path or name of the Whisper model to use (e.g., 'tiny', 'base', 'small')
    AUDIO_LOCATION: Directory path containing input WAV audio files
    JSON_OUTPUT: Directory path for intermediate JSON transcription files
    SRT_OUTPUT: Directory path for final SRT subtitle files

"""

import os
import glob

from whisper_hf_pipeline import hugging_face_speech2text_pipeline
from whisper_whispertimestamped import whispertimestamped_speech2text_pipeline
from srt_generator_hf import convert_json_to_srt_file


def main():
    """
    Main execution function for the speech-to-text pipeline.

    This function orchestrates the complete pipeline:
    1. Loads environment variables for configuration
    2. Discovers audio files in the input directory
    3. Processes audio files through speech-to-text transcription
    4. Converts JSON transcriptions to SRT subtitle format

    Raises:
        ValueError: If required environment variables are not set
        FileNotFoundError: If input directories don't exist
        PermissionError: If output directories are not writable
    """
    MODEL = os.getenv(
        "PT_MODEL_TINY"
    )  # tiny model used due to limited hardware capabilities
    AUDIO_LOCATION = os.getenv("AUDIO_LOCATION")
    JSON_OUTPUT = os.getenv("JSON_OUTPUT")
    SRT_OUTPUT = os.getenv("SRT_OUTPUT")

    AUDIO_FILE_LIST = glob.glob(AUDIO_LOCATION + "/*.wav")
    JSON_FILE_LIST = glob.glob(JSON_OUTPUT + "/*.json")

    hugging_face_speech2text_pipeline(AUDIO_FILE_LIST, MODEL, JSON_OUTPUT)
    convert_json_to_srt_file(JSON_FILE_LIST, SRT_OUTPUT)

    # whispertimestamped_speech2text_pipeline(AUDIO_FILE_LIST, MODEL, JSON_OUTPUT)


if __name__ == "__main__":
    main()
