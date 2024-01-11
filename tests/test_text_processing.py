import os
import sys

main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_folder_path)

from text_processing import (
    merge_repeats,
    split_acronym,
    split_acronyms,
    split_if_acronym,
)


def test_split_acronyms():
    text = "No acronyms to split. 10 Million people live in Portugal. OpenAI's Whisper is cool."
    assert split_acronyms(text) == text
    text = "There is an acronym to split. SLB1904. OIS300."
    assert (
        split_acronyms(text) == "There is an acronym to split. S L B 1904 . O I S 300 ."
    )


def test_split_acronym():
    word = "Lisbon"
    assert split_acronym(word) == word
    word = "SLB"
    assert split_acronym(word) == "S L B"
    word = "OIS300"
    assert split_acronym(word) == "O I S 300"


def test_split_if_acronym():
    segment = "Lisbon"
    assert split_if_acronym(segment) == segment
    segment = "SLB"
    assert split_if_acronym(segment) == "S L B"
    segment = "300"
    assert split_if_acronym(segment) == "300"


def test_merge_repeats():
    segments = [
        {"text": "No", "start": 0, "end": 1},
        {"text": "Repeats", "start": 2, "end": 3},
        {"text": "Here", "start": 4, "end": 5},
    ]
    assert merge_repeats(segments) == segments
    segments = [
        {"text": "Repeat", "start": 0, "end": 1},
        {"text": "Occurs", "start": 2, "end": 3},
        {"text": "Occurs", "start": 4, "end": 5},
    ]
    expected_merged_segments = [
        {"text": "Repeat", "start": 0, "end": 1},
        {"text": "Occurs", "start": 2, "end": 5},
    ]
    assert merge_repeats(segments) == expected_merged_segments
    segments = [
        {"text": "Repeat Occurs", "start": 0, "end": 1},
        {"text": "Repeat Occurs", "start": 2, "end": 3},
        {"text": "Occurs", "start": 4, "end": 5},
    ]
    expected_merged_segments = [
        {"text": "Repeat Occurs", "start": 0, "end": 5},
    ]
    assert merge_repeats(segments) == expected_merged_segments
    segments = [
        {"text": "Repeat Occurs", "start": 0, "end": 1},
        {"text": "Repeat Occurs", "start": 2, "end": 3},
        {"text": "Whatever", "start": 3.1, "end": 3.7},
        {"text": "Occurs", "start": 4, "end": 5},
    ]
    expected_merged_segments = [
        {"text": "Repeat Occurs", "start": 0, "end": 3},
        {"text": "Whatever", "start": 3.1, "end": 3.7},
        {"text": "Occurs", "start": 4, "end": 5},
    ]
    assert merge_repeats(segments) == expected_merged_segments