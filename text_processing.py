import re
from string import ascii_uppercase
from typing import Union


def split_acronyms(text: str) -> str:
    words = [split_acronym(word) for word in text.split()]

    return " ".join(words).strip()


def split_acronym(word: str) -> str:
    characters_or_digits = r"\d+|\D+"
    segments = re.findall(characters_or_digits, word)
    segments = [split_if_acronym(segment) for segment in segments]
    return " ".join(segments).strip()


def split_if_acronym(segment: str) -> str:
    if all([letter in ascii_uppercase for letter in segment]):
        return " ".join(list(segment)).strip()
    else:
        return segment


def merge_repeats(segments: list[dict[str, Union[str, float]]]) -> list[dict]:
    segments_merged = [segments[0]]
    for segment in segments[1:]:
        if next_segment_text_is_substring(segments_merged[-1], segment):
            segments_merged[-1]["end"] = segment["end"]
        else:
            segments_merged.append(segment)
    return segments_merged


def next_segment_text_is_substring(
    last_segment: dict[str, Union[str, float]], segment: dict[str, Union[str, float]]
):
    next_segment_text = segment["text"].strip()
    last_segment_text = last_segment["text"].strip()
    return last_segment_text[-len(next_segment_text) :] == next_segment_text


def merge_on_interpunction(segments: list[dict[str, Union[str, float]]]) -> list[dict]:
    INTERPUNCTION = ",.?!:"
    segments_merged = [segments[0]]
    for segment in segments[1:]:
        if segments_merged[-1]["text"].strip()[-1] in INTERPUNCTION:
            segments_merged.append(segment)
        else:
            segments_merged[-1][
                "text"
            ] = f"{segments_merged[-1]['text'].strip()} {segment['text'].strip()}"
            segments_merged[-1]["end"] = segment["end"]
    return segments_merged
