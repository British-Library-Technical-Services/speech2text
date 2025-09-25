from typing import Tuple, List, TextIO
import os
import json


def extract_json_data(file: str) -> str:
    data: str = None
    try:
        with open(file) as f:
            data = json.load(f)
            return data

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error in {file}: {e}")
        return


def get_timecode_data(data: dict, index: int) -> Tuple[str, str, str]:
    start_time = data["timestamp"][0]
    end_time = data["timestamp"][1]
    text = data["text"]

    return start_time, end_time, text


def time_conversion(start: str, end: str) -> Tuple[str, str]:
    if start is None or end is None:
        print("Invalid timestamp data: 'null' found")
        return None, None

    start_hours = start // 3600
    start_minutes = (start % 3600) // 60
    start_seconds = start % 60
    start_milliseconds = round((start % 1) * 1000)

    end_hours = end // 3600
    end_minutes = (end % 3600) // 60
    end_seconds = end % 60
    end_milliseconds = round((end % 1) * 1000)

    start_time = f"{int(start_hours):02}:{int(start_minutes):02}:{int(start_seconds):02},{int(start_milliseconds):03}"
    end_time = f"{int(end_hours):02}:{int(end_minutes):02}:{int(end_seconds):02},{int(end_milliseconds):03}"

    return start_time, end_time


def srt_line_formatter(
    start_time: str, end_time: str, text: str, index: int
) -> List[str]:
    subtitle: str = None
    if not start_time or not end_time:
        subtitle = f"NOTE {index}\n{start_time} --> {end_time}\n{text.strip()}\n\n"

    subtitle = f"{index}\n{start_time} --> {end_time}\n{text.strip()}\n\n"
    return subtitle


def write_srt_file(
    json_file: str, subtitle_output: str, subtitles: List[str]
) -> TextIO:
    subtitle_file: TextIO = None
    srt_name = os.path.basename(json_file).replace(".json", ".srt")
    srt_file = os.path.join(subtitle_output, srt_name)

    try:
        with open(srt_file, "w", encoding="utf-8") as subtitle_file:
            for line in subtitles:
                subtitle_file.write(line)
        return subtitle_file

    except IOError as e:
        print(f"Error writing to {srt_file}: {e}")
