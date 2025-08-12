# Speech-to-Text Processing Pipeline

A Python-based speech-to-text transcription service that converts audio files to timestamped transcriptions and generates SRT subtitle files using OpenAI's Whisper models via multiple implementation approaches.

---
## Table of Contents
1. Overview
2. Core Workflows
3. Architecture
4. Environment & Dependencies
5. Setup
6. Usage
7. File & Naming Conventions
8. Output Formats

---
## 1. Overview
The service provides automated speech-to-text transcription with:
- Support for multiple Whisper model implementations (Hugging Face Transformers, Whisper Timestamped).
- Batch processing of WAV audio files with progress tracking.
- Automatic generation of timestamped JSON transcriptions and SRT subtitle files.
- Configurable model selection based on hardware capabilities and accuracy requirements.
- Error handling and recovery for robust batch operations.

## 2. Core Workflows
### 2.1 Standard Transcription Pipeline (Hugging Face)
Steps:
1. Load environment configuration and validate required variables.
2. Discover WAV audio files in the input directory.
3. Process each audio file through Hugging Face Transformers pipeline.
4. Generate timestamped JSON transcription files with phrase-level timestamps.
5. Convert JSON files to SRT subtitle format with proper time formatting.

### 2.2 Enhanced Precision Pipeline (Whisper Timestamped)
1. Load Whisper model with enhanced timestamp capabilities.
2. Process audio files with word-level timestamp precision.
3. Generate detailed JSON transcriptions with improved timing accuracy.
4. Convert to SRT format maintaining high-precision timestamps.
5. Suitable for applications requiring exact word-level synchronization.

## 3. Architecture
Module | Responsibility
-------|---------------
`main.py` | Orchestrates transcription workflow & environment setup
`whisper_hf_pipeline.py` | Hugging Face Transformers implementation with batch processing
`whisper_whispertimestamped.py` | Enhanced timestamp precision using whisper-timestamped
`srt_generator_hf.py` | JSON to SRT conversion with time formatting

## 4. Environment & Dependencies
Python: 3.8+
Required Python packages:
- transformers
- torch
- tqdm
- whisper-timestamped (optional, for enhanced precision)

Environment variables (create `.env` file):
```
PT_MODEL_TINY        # Whisper model name ('tiny', 'base', 'small', 'medium', 'large')
AUDIO_LOCATION       # Directory containing input WAV files
JSON_OUTPUT          # Directory for intermediate JSON transcriptions
SRT_OUTPUT           # Directory for final SRT subtitle files
```

## 5. Setup
```bash
git clone https://github.com/British-Library-Technical-Services/speech2text.git
cd speech2text
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install transformers torch tqdm
pip install whisper-timestamped  # Optional for enhanced precision
cp .env.example .env  # Create and edit environment file
```

## 6. Usage
Run transcription pipeline:
```bash
python main.py
```

The service will:
1. Load configuration from environment variables
2. Discover all `.wav` files in `AUDIO_LOCATION`
3. Process files through the selected pipeline
4. Generate JSON transcriptions in `JSON_OUTPUT`
5. Create SRT subtitle files in `SRT_OUTPUT`

## 7. File & Naming Conventions
Item | Convention
-----|-----------
Input audio files | `.wav` format (other formats may require conversion)
JSON transcriptions | `<original_filename>_hfpipeline.json` or `<original_filename>_timestamped.json`
SRT subtitle files | `<original_filename>.srt`
Model names | `tiny`, `base`, `small`, `medium`, `large` (increasing accuracy/size)

## 8. Output Formats
### 8.1 JSON Transcription Format
```json
[
  {
    "timestamp": [10.5, 15.2],
    "text": "This is the transcribed text segment"
  }
]
```

### 8.2 SRT Subtitle Format
```
1
00:00:10,500 --> 00:00:15,200
This is the transcribed text segment

2
00:00:15,200 --> 00:00:20,100
Next subtitle segment
```
