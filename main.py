from typing import List
from dotenv import load_dotenv
import os
import glob

from tqdm import tqdm

from whisper_hf_pipeline import transcribe_speech, write_transcript_json_file
from srt_generator_hf import (
    extract_json_data,
    get_timecode_data,
    time_conversion,
    srt_line_formatter,
    write_srt_file,
)

env_varibles = load_dotenv()
# print(f".env variables successfully loaded {env_varibles}")


def validate_locations(model: str, audio: str, json: str, srt: str) -> bool:
    if not os.path.exists(model):
        print(f"Error: No whisper model found - exiting")
        return
    print("\u2713 Whisper ASR model found")

    if not os.path.exists(audio):
        os.mkdir(audio)
        print(f"... created directory for audio_files at {audio}")
    print(f"\u2713 audio file directory {audio}")

    if not os.path.exists(json):
        os.mkdir(json)
        print(f"... created directory for json output at {json}")
    print(f"\u2713 json output directory {json}")

    if not os.path.exists(srt):
        os.mkdir(srt)
        print(f"... created directory for json output at {srt}")
    print(f"\u2713 srt subtitle output directory {srt}")


def generate_json_transcripts(
    model: str, audio_files_location: str, json_file_write_location: str
) -> List[str]:
    failed_transcription: List[str] = []

    audio_files_to_transcribe = glob.glob(os.path.join(audio_files_location, "*.wav"))
    if not audio_files_to_transcribe:
        print(f"No audio files found in {audio_files_location} - exiting")
        return

    for audio_file in tqdm(audio_files_to_transcribe):
        valid_transcription = transcribe_speech(
            audio_file=audio_file, asr_model=model, json_output=json_file_write_location
        )
        if not valid_transcription:
            failed_transcription.append(audio_file)
            continue

        json_transcript = write_transcript_json_file(
            transcription=valid_transcription,
            audio_file=audio_file,
            json_output=json_file_write_location,
        )
        if not json_transcript:
            failed_transcription(audio_file)
            continue

    return failed_transcription


def transcode_transcript_to_subtitle(
    json_files_location: str, srt_file_write_location: str
) -> List[str]:
    failed_subtitle_file: list[str] = []

    json_files_to_transcode_to_srt = glob.glob(
        os.path.join(json_files_location, "*.json")
    )
    if not json_files_to_transcode_to_srt:
        print(f"No json files found in {json_files_to_transcode_to_srt} - exiting")
        return

    for count, json_file in enumerate(json_files_to_transcode_to_srt):

        print(
            "Converting JSON > SRT:",
            count + 1,
            "of",
            len(json_files_to_transcode_to_srt),
        )
        extracted_json = extract_json_data(file=json_file)
        if not extracted_json:
            failed_subtitle_file.append(json_file)
            continue

        subtitles: List[str] = []
        for index, data in enumerate(extracted_json):
            start_time, end_time, subtitle = get_timecode_data(data=data, index=index)
            converted_start_time, converted_end_time = time_conversion(
                start=start_time, end=end_time
            )

            srt_data = srt_line_formatter(
                start_time=converted_start_time,
                end_time=converted_end_time,
                text=subtitle,
                index=index,
            )
            if not srt_data:
                failed_subtitle_file.append(json_file)
                continue
            subtitles.append(srt_data)

        srt_subtitle = write_srt_file(
            json_file=json_file,
            subtitle_output=srt_file_write_location,
            subtitles=subtitles,
        )
        if not srt_subtitle:
            failed_subtitle_file.append(json_file)

    return failed_subtitle_file


def main():
    model = os.getenv("HF_MODEL_TINY")
    audio_files_location = os.getenv("AUDIO_LOCATION")
    json_file_write_location = os.getenv("JSON_OUTPUT")
    srt_file_write_location = os.getenv("SRT_OUTPUT")

    print("Validating service locations exist")
    validate_locations(
        model=model,
        audio=audio_files_location,
        json=json_file_write_location,
        srt=srt_file_write_location,
    )

    print("Transcribing speech to text")
    failed_transcription = generate_json_transcripts(
        model=model,
        audio_files_location=audio_files_location,
        json_file_write_location=json_file_write_location,
    )
    if len(failed_transcription) > 0:
        print(f"{len(failed_transcription)} transcripts failed to generate")
        for transcript in failed_transcription:
            print(f"* {transcript}")

    print("Transcoding transcript to srt subtitle file")
    failed_subtitle = transcode_transcript_to_subtitle(
        json_files_location=json_file_write_location,
        srt_file_write_location=srt_file_write_location,
    )
    if len(failed_subtitle) > 0:
        print(f"{len(failed_subtitle)} subtitle files failed to be generated")
        for subtitle in failed_subtitle:
            print(f"* {subtitle}")


if __name__ == "__main__":
    main()
