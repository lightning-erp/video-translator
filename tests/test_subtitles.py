import os
import sys

main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_folder_path)


import pysrt

from subtitles import seconds_to_hms


def test_time_parsing_for_pysrt():
    time = 13.0
    time_parsed = seconds_to_hms(time)
    assert time_parsed == "0:00:13,000"

    time = 71.0
    time_parsed = seconds_to_hms(time)
    assert time_parsed == "0:01:11,000"

    time = 4761.0
    time_parsed = seconds_to_hms(time)
    assert time_parsed == "1:19:21,000"

    start = 21.0
    end = 71.0
    srt = pysrt.SubRipItem(
        start=seconds_to_hms(start), end=seconds_to_hms(end), text=""
    )
    assert srt.duration == f"00:00:50,000"
