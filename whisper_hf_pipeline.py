"""
Hugging Face Transformers Speech-to-Text Pipeline

This module provides speech-to-text transcription functionality using the Hugging Face
Transformers library. It implements an automatic speech recognition pipeline that
processes audio files and generates timestamped JSON transcriptions.

The module is optimized for CPU inference with chunked processing to handle longer
audio files.
"""

from transformers import pipeline
import os
import json
from tqdm import tqdm


def transcribe_speech(audio_file, MODEL, JSON_OUTPUT):
    """
    Transcribe an audio file using Hugging Face Transformers pipeline.

    This function processes a single WAV audio file through the automatic speech
    recognition pipeline, extracting both text transcriptions and timestamps.
    The results are saved as a JSON file with timestamped chunks.

    Args:
        audio_file (str): Absolute path to the input WAV audio file
        MODEL (str): Name or path of the Whisper model to use (e.g., 'tiny', 'base', 'small')
        JSON_OUTPUT (str): Directory path where the output JSON file will be saved

    Returns:
        None: Results are written directly as JSON files

    Raises:
        Exception: If speech recognition pipeline fails during prediction
        IOError: If unable to write the output JSON file

    Note:
        - Uses CPU device for inference with chunk_length_s=20 for memory efficiency
        - Output filename format: {original_filename}_hfpipeline.json
        - Batch size is set to 8 for optimal CPU performance
    """
    pipe = pipeline(
        "automatic-speech-recognition",
        model=MODEL,
        chunk_length_s=20,
        device="cpu",
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
    """
    Process multiple audio files through the Hugging Face speech-to-text pipeline.

    This function orchestrates the transcription of multiple audio files by calling
    the transcribe_speech function for each file. Progress is displayed using a
    progress bar to provide user feedback during batch processing.

    Args:
        FILE_LIST (list): List of absolute paths to WAV audio files to be processed
        MODEL (str): Name or path of the Whisper model to use for transcription
        JSON_OUTPUT (str): Directory path where output JSON files will be saved
    """
    for file in tqdm(FILE_LIST, desc="Transcribing Audio Files"):
        transcribe_speech(file, MODEL, JSON_OUTPUT)
