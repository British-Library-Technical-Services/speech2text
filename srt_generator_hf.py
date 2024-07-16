import os
import glob
import json

JSON_FILES = os.getenv("JSON_OUTPUT")
SRT_OUTPUT = os.getenv("SRT_OUTPUT")

FILE_LIST = glob.glob(JSON_FILES + "/*.json")

def get_timecode_text(data, index):
    start_time = data[index]["timestamp"][0]
    end_time = data[index]["timestamp"][1]
    text = data[index]["text"]
    
    return start_time, end_time, text
    
def time_conversion(start, end):
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


def srt_line_formatter(start_time, end_time, text, index):
    index += 1
    line = f"{index}\n{start_time} --> {end_time}\n{text.strip()}\n\n"
    return line


for count, file in enumerate(FILE_LIST):
    print("Converting JSON > SRT:", count + 1, "of", len(FILE_LIST))
    with open(file) as f:
        data = json.load(f)

    srt_name = os.path.basename(file).replace(".json", ".srt")
    srt_file = os.path.join(SRT_OUTPUT, srt_name)
    
    for index, value in enumerate(data):
        start, end, text = get_timecode_text(data, index)
        start_time, end_time = time_conversion(start, end)
        line = srt_line_formatter(start_time, end_time, text, index)
    
        
        with open(srt_file, "a") as f:
            f.write(line)