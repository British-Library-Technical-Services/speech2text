# Speech-to-Text Processing Pipeline

A robust Python-based speech-to-text transcription service that converts WAV audio files to timestamped JSON transcriptions and generates SRT subtitle files using OpenAI's Whisper models via Hugging Face Transformers.

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [Setup & Installation](#setup--installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Processing Pipeline](#processing-pipeline)
8. [Output Formats](#output-formats)
9. [Troubleshooting](#troubleshooting)

## Overview

This service provides automated batch processing of audio files with the following capabilities:

- **Batch Processing**: Processes multiple WAV files from a specified directory
- **Timestamped Transcription**: Generates JSON files with precise timestamp information
- **SRT Subtitle Generation**: Converts JSON transcriptions to standard SRT subtitle format
- **Progress Tracking**: Visual progress bars for batch operations using tqdm
- **Error Handling**: Comprehensive error handling with detailed logging
- **Directory Management**: Automatic creation of required output directories

## Project Structure

```
speech2text/
├── main.py                          # Main orchestration script
├── whisper_hf_pipeline.py          # Hugging Face Transformers implementation
├── whisper_whispertimestamped.py   # Alternative Whisper implementation
├── srt_generator_hf.py             # JSON to SRT conversion utilities
├── _directories/
│   ├── _models/                    # Downloaded Whisper models cache
│   ├── audio/                      # Input WAV files
│   │   └── done/                   # Processed audio files
│   ├── json_output/                # Generated JSON transcriptions
│   └── srt_output/                 # Generated SRT subtitle files
│       └── done/                   # Processed SRT files
└── README.md                       # This file
```

### Core Modules

| Module | Purpose |
|--------|---------|
| `main.py` | Application entry point, orchestrates the entire workflow |
| `whisper_hf_pipeline.py` | Handles speech-to-text transcription using Hugging Face pipeline |
| `srt_generator_hf.py` | Converts JSON transcriptions to SRT format with proper time formatting |
| `whisper_whispertimestamped.py` | Alternative implementation for enhanced timestamp precision |

## Requirements

- **Python**: 3.8 or higher
- **Required Packages**:
  - `transformers` - Hugging Face Transformers library
  - `torch` - PyTorch for model inference
  - `tqdm` - Progress bars for batch operations
  - `python-dotenv` - Environment variable management

## Setup & Installation

1. **Clone the repository**:
   ```powershell
   git clone https://github.com/British-Library-Technical-Services/speech2text.git
   cd speech2text
   ```

2. **Create and activate virtual environment**:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```powershell
   pip install transformers torch tqdm python-dotenv
   ```

4. **Create environment configuration**:
   Create a `.env` file in the project root with the required environment variables (see Configuration section).

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Whisper model configuration
HF_MODEL_TINY=openai/whisper-tiny.en

# Directory paths (use absolute paths for reliability)
AUDIO_LOCATION=C:\_development\speech2text\_directories\audio
JSON_OUTPUT=C:\_development\speech2text\_directories\json_output
SRT_OUTPUT=C:\_development\speech2text\_directories\srt_output
```

### Model Options
- `openai/whisper-tiny.en` - Fastest, lowest accuracy, English-only
- `openai/whisper-small.en` - Balanced speed/accuracy, English-only
- `openai/whisper-small` - Multilingual support
- `openai/whisper-base` - Better accuracy, slower processing
- `openai/whisper-medium` - High accuracy, requires more resources
- `openai/whisper-large` - Highest accuracy, slowest processing

## Usage

1. **Place audio files**: Copy your `.wav` files to the audio input directory specified in `AUDIO_LOCATION`

2. **Run the pipeline**:
   ```powershell
   python main.py
   ```

3. **Monitor progress**: The application will display progress bars and status updates for each processing stage

4. **Check outputs**: 
   - JSON transcriptions will be saved to `JSON_OUTPUT`
   - SRT subtitle files will be saved to `SRT_OUTPUT`

## Processing Pipeline

The application follows this workflow:

### 1. Environment Validation
- Loads environment variables from `.env` file
- Validates that the Whisper model exists (downloads if necessary)
- Creates output directories if they don't exist

### 2. Audio Processing
- Scans the audio directory for `.wav` files
- Processes each file through the Hugging Face Transformers pipeline
- Generates timestamped JSON transcription files

### 3. SRT Generation
- Reads existing JSON transcription files
- Extracts timestamp and text data
- Converts timestamps to SRT format (HH:MM:SS,mmm)
- Generates properly formatted SRT subtitle files

### Error Handling
- Tracks failed transcriptions and subtitle generations
- Provides detailed error reporting
- Continues processing remaining files if individual files fail

## Output Formats

### JSON Transcription Format
```json
[
  {
    "timestamp": [10.5, 15.2],
    "text": "This is the transcribed text segment"
  },
  {
    "timestamp": [15.2, 20.1], 
    "text": "Next transcription segment"
  }
]
```

### SRT Subtitle Format
```srt
1
00:00:10,500 --> 00:00:15,200
This is the transcribed text segment

2
00:00:15,200 --> 00:00:20,100
Next transcription segment
```


