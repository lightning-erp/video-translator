from datetime import timedelta
from typing import Union
import os
from pysrt import SubRipFile, SubRipItem


def save_to_srt(transctipt: list[dict[str, Union[float, str]]], output: str):
    items = [create_subripitem(segment) for segment in transctipt]
    subtitles = SubRipFile(items)
    output_file = output if ".srt" in output else f"{output}.srt"
    try:
        subtitles.save(output_file)
    except FileNotFoundError:
        output_file_path = "/".join(output_file.split("/")[:-1])
        os.makedirs(output_file_path)
    print(f"translated transcription saved to {output_file}")


def create_subripitem(segment: dict[str, Union[float, str]]) -> SubRipItem:
    print(segment)
    start = seconds_to_hms(segment["start"])
    end = seconds_to_hms(segment["end"])
    text = segment["text"]
    print(start, end)
    print(segment["start"], segment["end"])

    return SubRipItem(start=start, end=end, text=text)


def seconds_to_hms(seconds: float) -> str:
    hms = str(timedelta(seconds=seconds))
    ms = ".000000" if "." not in hms else ""
    return hms + ms
