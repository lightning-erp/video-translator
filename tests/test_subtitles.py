import os
import sys

import pytest

main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_folder_path)


import pysrt

from subtitles import save_to_srt, seconds_to_hms


def test_time_parsing_no_millis():
    time = 13.0
    time_parsed = seconds_to_hms(time)
    assert time_parsed == "0:00:13.000000"


def test_time_parsing_with_millis():
    time = 71.351
    time_parsed = seconds_to_hms(time)
    assert time_parsed == "0:01:11.351000"


def test_time_parsing_over_1h():
    time = 4761.3
    time_parsed = seconds_to_hms(time)
    assert time_parsed == "1:19:21.300000"


def test_creating_subripitem():
    start = 21.0
    end = 71.0
    srt = pysrt.SubRipItem(
        start=seconds_to_hms(start), end=seconds_to_hms(end), text=""
    )
    assert srt.duration == f"00:00:50,000"


@pytest.fixture
def test_save_to_srt_fixture():
    transcript = [
        {"start": 0, "end": 21, "text": "lx"},
        {"start": 21, "end": 71, "text": "7r"},
    ]
    output_file_path = "test.srt"

    yield transcript, output_file_path

    os.remove(output_file_path)


def test_save_to_srt(test_save_to_srt_fixture):
    transcript, output_file_path = test_save_to_srt_fixture
    save_to_srt(transcript, output_file_path)
