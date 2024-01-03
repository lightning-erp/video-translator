import os
import sys

main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_folder_path)

from voiceover import get_video_length


def test_get_video_length():
    length = get_video_length(os.path.join(main_folder_path, "tests", "test.mp4"))
    assert length == 10000
