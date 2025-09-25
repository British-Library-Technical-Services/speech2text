"""
Whisper Timestamped Speech-to-Text Pipeline

This module provides an alternative speech-to-text transcription implementation
using the whisper-timestamped library. It offers more precise timestamp alignment
compared to the standard Hugging Face pipeline, making it suitable for applications
requiring high-accuracy subtitle generation.

The module processes audio files using OpenAI's Whisper models with enhanced
timestamp precision, generating detailed transcription data with word-level timing.

Dependencies:
    - whisper-timestamped: Enhanced Whisper implementation with precise timestamps
    - json: For JSON output formatting
    - os: For file path operations

"""

import os
import whisper_timestamped as whisper
import json


def transcribe_speech(audio_file, MODEL, JSON_OUTPUT):
    """
    Transcribe a single audio file using Whisper Timestamped.

    This function processes a single WAV audio file using the whisper-timestamped
    library, which provides enhanced timestamp accuracy compared to standard Whisper.
    The transcription is performed with English language detection and results
    are saved as detailed JSON files.

    Args:
        audio_file (str): Absolute path to the input WAV audio file
        MODEL (str): Name of the Whisper model to use (e.g., 'tiny', 'base', 'small')
        JSON_OUTPUT (str): Directory path where the output JSON file will be saved

    Returns:
        None: Results are written directly to disk as JSON files

    Raises:
        Exception: If Whisper transcription fails during processing
        IOError: If unable to write the output JSON file

    """
    load_model = whisper.load_model(MODEL)
    load_audio = whisper.load_audio(audio_file)

    output = None  # Initialize output
    try:
        transcribe = whisper.transcribe(load_model, load_audio, language="en")
        output = json.dumps(transcribe, indent=2)
    except Exception as e:
        print(f"Prediction Error: {e}")
        return  # Return early if transcription fails

    filename = os.path.basename(audio_file).replace(".m4a", ".json")

    try:
        with open(os.path.join(JSON_OUTPUT, filename), "w") as f:
            f.write(output)
    except IOError as e:
        print(f"File Write Error: {e}")


def whispertimestamped_speech2text_pipeline(FILE_LIST, MODEL, JSON_OUTPUT):
    """
    Process multiple audio files through the Whisper Timestamped pipeline.

    This function orchestrates the transcription of multiple audio files using
    the whisper-timestamped library. Each file is processed sequentially to
    generate high-precision timestamped transcriptions.

    Args:
        FILE_LIST (list): List of absolute paths to WAV audio files to be processed
        MODEL (str): Name of the Whisper model to use for transcription
        JSON_OUTPUT (str): Directory path where output JSON files will be saved

    Returns:
        None: Results are written to disk for each processed file

    Note:
        - Processes files sequentially without progress bar (unlike HF pipeline)
        - Each file generates a separate JSON file with enhanced timestamp data
        - Failed transcriptions are logged but don't stop the batch process

    Example:
        >>> audio_files = ['/path/to/audio1.wav', '/path/to/audio2.wav']
        >>> whispertimestamped_speech2text_pipeline(audio_files, 'tiny', '/output/dir')
    """
    for file in FILE_LIST:
        transcribe_speech(file, MODEL, JSON_OUTPUT)
