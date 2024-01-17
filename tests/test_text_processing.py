import os
import sys

main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_folder_path)

from text_processing import (
    add_missing_interpunction,
    merge_on_interpunction,
    merge_repeats,
    split_acronym,
    split_acronyms,
    split_if_acronym,
    split_on_interpunction,
)


def test_split_acronyms():
    text = "No acronyms to split. 10 Million people live in Portugal. OpenAI's Whisper is cool."
    assert split_acronyms(text) == text
    text = "There is an acronym to split. SLB1904. OIS300."
    assert (
        split_acronyms(text) == "There is an acronym to split. S L B 1904 . O I S 300 ."
    )
    text = ""
    assert split_acronyms(text) == text


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
    segments = []
    assert merge_repeats(segments) == segments
    segments = [
        {
            "text": "The OIS302 application is a very useful application.",
            "start": 0,
            "end": 1,
        },
        {
            "text": "We can see that the OIS302 application is a very useful application.",
            "start": 1,
            "end": 2,
        },
        {
            "text": "The OIS302 application is a very useful application.",
            "start": 3,
            "end": 4,
        },
    ]
    expected_merged_segments = [
        {
            "text": "We can see that the OIS302 application is a very useful application.",
            "start": 0,
            "end": 4,
        },
    ]
    assert merge_repeats(segments) == expected_merged_segments


def test_merge_on_interpunction():
    segments = []
    assert merge_on_interpunction([]) == []
    segments = [
        {"text": "No broken sentences.", "start": 0, "end": 1},
        {"text": "Whisper identified it all correctly, ", "start": 2, "end": 3},
        {"text": "so nothing will change.", "start": 4, "end": 5},
    ]
    assert merge_on_interpunction(segments) == segments
    segments = [
        {"text": "There are broken sentences.", "start": 0, "end": 1},
        {"text": "Whisper identified some ", "start": 2, "end": 3},
        {"text": " of them wrong.", "start": 4, "end": 5},
    ]
    expected_merged_segments = [
        {"text": "There are broken sentences.", "start": 0, "end": 1},
        {"text": "Whisper identified some of them wrong.", "start": 2, "end": 5},
    ]
    assert merge_on_interpunction(segments) == expected_merged_segments
    segments = []
    assert merge_on_interpunction(segments) == []
    segments = [
        {"text": "There are broken sentences.", "start": 0, "end": 1},
        {"text": "Whisper identified some ", "start": 2, "end": 3},
        {"text": " of them wrong.", "start": 4, "end": 5},
    ]
    expected_merged_segments = [
        {"text": "There are broken sentences.", "start": 0, "end": 1},
        {"text": "Whisper identified some of them wrong.", "start": 2, "end": 5},
    ]
    assert merge_on_interpunction(segments) == expected_merged_segments
    segments = [
        {
            "start": 13,
            "end": 14,
            "text": "If you already have basic knowledge how to use M3 system",
        },
        {
            "start": 14,
            "end": 15,
            "text": "Let's move to the question how to order goods",
        },
        {
            "start": 15,
            "end": 16,
            "text": "To order goods we need two basic information",
        },
        {
            "start": 16,
            "end": 17,
            "text": "These are the contract data and the item data",
        },
        {
            "start": 17,
            "end": 18,
            "text": "These two information will be combined with the price tag which will fill us with information about how much this specified product costs at this specific contractor",
        },
        {
            "start": 18,
            "end": 19,
            "text": "Above text will put length of text over the limit so this should split now",
        },
    ]
    expected_merged_segments = [
        {
            "start": 13,
            "end": 18,
            "text": "If you already have basic knowledge how to use M3 system Let's move to the question how to order goods To order goods we need two basic information These are the contract data and the item data These two information will be combined with the price tag which will fill us with information about how much this specified product costs at this specific contractor",
        },
        {
            "start": 18,
            "end": 19,
            "text": "Above text will put length of text over the limit so this should split now",
        },
    ]
    assert merge_on_interpunction(segments) == expected_merged_segments


def test_add_missing_interpunction():
    segment = {
        "text": "No missing interpunction.",
        "start": 0,
        "end": 11,
    }
    assert add_missing_interpunction(segment) == segment
    segment = {
        "text": "There is missing interpunction Therefore it will be fixed.",
        "start": 0,
        "end": 11,
    }
    expected_segment = {
        "text": "There is missing interpunction, Therefore it will be fixed.",
        "start": 0,
        "end": 11,
    }
    assert add_missing_interpunction(segment) == expected_segment


def OBSOLETE_test_split_on_interpunction():
    assert False
    segments = [
        {
            "text": "No missing interpunction.",
            "start": 0,
            "end": 3,
        }
    ]
    assert split_on_interpunction(segments) == segments
    segments = [
        {
            "text": "There is missing interpunction Therefore it will be fixed.",
            "start": 0,
            "end": 11,
        }
    ]
    expected_split_segments = [
        {
            "text": "There is missing interpunction,",
            "start": 0,
            "end": 6.3,
        },
        {
            "text": "Therefore it will be fixed.",
            "start": 6.3,
            "end": 11,
        },
    ]
    assert split_on_interpunction(segments) == expected_split_segments
    segments = []
    assert split_on_interpunction(segments) == segments
    segments = [
        {
            "text": "There is proper interpunction, therefore it will be not be changed.",
            "start": 0,
            "end": 11,
        }
    ]
    expected_split_segments = [
        {
            "text": "There is proper interpunction,",
            "start": 0,
            "end": 5.7,
        },
        {
            "text": "therefore it will be not be changed.",
            "start": 5.7,
            "end": 11,
        },
    ]
    assert split_on_interpunction(segments) == expected_split_segments
