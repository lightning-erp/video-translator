import re
from string import ascii_uppercase
from typing import Union

import phonetics

INTERPUNCTION = ",.?!:"


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
    try:
        segments_merged = [segments[0]]
    except IndexError:
        return segments
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
    try:
        segments_merged = [segments[0]]
    except IndexError:
        return segments
    for segment in segments[1:]:
        if segments_merged[-1]["text"].strip()[-1] in INTERPUNCTION:
            segments_merged.append(segment)
        else:
            segments_merged[-1][
                "text"
            ] = f"{segments_merged[-1]['text'].strip()} {segment['text'].strip()}"
            segments_merged[-1]["end"] = segment["end"]
    return segments_merged


def split_on_interpunction(segments: list[dict[str, Union[str, float]]]) -> list[dict]:
    split_segments = list()
    for segment in segments:
        segment_with_interpunction = add_missing_interpunction(segment)
        segment_sounds_length = len(
            phonetics.metaphone(segment_with_interpunction["text"])
        )
        if segment_sounds_length == 0:
            split_segments.append(segment)
            continue
        segment_length = segment["end"] - segment["start"]
        new_texts: list[str] = re.findall(
            r"[^.,\-:]+(?:[.,\-:]|\b)", segment_with_interpunction["text"]
        )

        subsegment_length = get_subsegment_length(
            segment_sounds_length, segment_length, new_texts[0]
        )
        subsegments = [
            {
                "text": new_texts[0],
                "start": segment["start"],
                "end": round(
                    segment["start"] + subsegment_length,
                    1,
                ),
            }
        ]
        for text in new_texts[1:]:
            subsegment_length = get_subsegment_length(
                segment_sounds_length, segment_length, text
            )
            subsegments.append(
                {
                    "text": text.strip(),
                    "start": subsegments[-1]["end"],
                    "end": subsegments[-1]["end"] + subsegment_length,
                }
            )
        split_segments.extend(subsegments)

    return split_segments


def get_subsegment_length(segment_sounds_length, segment_length, text):
    text_sounds = len(phonetics.metaphone(text))
    subsegment_length = round((text_sounds / segment_sounds_length) * segment_length, 1)

    return subsegment_length


def add_missing_interpunction(segment: dict[str, Union[str, float]]) -> dict:
    whitespace_uppercase_lowercase = r"(\s)([A-Z][a-z])"
    dot_before_whitespacee = r",\1\2"
    new_text = re.sub(
        whitespace_uppercase_lowercase, dot_before_whitespacee, segment["text"]
    )
    return {"text": new_text, "start": segment["start"], "end": segment["end"]}
