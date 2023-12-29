from datetime import timedelta
from typing import Union

from pysrt import SubRipFile, SubRipItem, SubRipTime


def save_to_srt(transctipt: list[dict[str, Union[float, str]]], output: str):
    items = [create_subripitem(segment) for segment in transctipt]
    subtitles = SubRipFile(items)
    subtitles.save(output if ".txt" in output else f"{output}.srt")


def create_subripitem(segment: dict[str, Union[float, str]]) -> SubRipItem:
    start = seconds_to_hms(segment["start"])
    end = seconds_to_hms(segment["end"])
    text = segment["text"]
    return SubRipItem(start=start, end=end, text=text)


def seconds_to_hms(seconds: float) -> str:
    return str(timedelta(seconds=seconds)) + ",000"
