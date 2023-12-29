from datetime import timedelta
from typing import Union

from pysrt import SubRipFile, SubRipItem


def save_to_srt(transctipt: list[dict[str, Union[float, str]]], output: str):
    items = [create_subripitem(segment) for segment in transctipt]
    subtitles = SubRipFile(items)
    output_file = output if ".txt" in output else f"{output}.srt"
    subtitles.save(output_file)
    print(f"translated transcription saved to {output_file}")


def create_subripitem(segment: dict[str, Union[float, str]]) -> SubRipItem:
    start = seconds_to_hms(segment["start"])
    end = seconds_to_hms(segment["end"])
    text = segment["text"]
    return SubRipItem(start=start, end=end, text=text)


def seconds_to_hms(seconds: float) -> str:
    return str(timedelta(seconds=seconds)) + ",000"
