import os
import shutil
import sys
from time import sleep

import pytest

main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_folder_path)

from drive_io import copy_directory_structure, dont_skip_dir, list_videos

IN_DIRECTORY = os.path.join(main_folder_path, "tests", "directories_test_dir", "in")
OUT_DIRECTORY = os.path.join(main_folder_path, "tests", "directories_test_dir", "out")


@pytest.fixture
def test_copy_directory_structure_fixture():
    try:
        shutil.rmtree(OUT_DIRECTORY)
    except FileNotFoundError:
        pass
    sleep(0.1)
    yield IN_DIRECTORY, OUT_DIRECTORY
    sleep(0.1)
    try:
        shutil.rmtree(OUT_DIRECTORY)
    except FileNotFoundError:
        pass


def test_copy_directory_structure_no_skip(test_copy_directory_structure_fixture):
    in_directory, out_directory = test_copy_directory_structure_fixture
    copy_directory_structure(in_directory, out_directory)

    in_dir = set()
    for path, directories, files in os.walk(in_directory):
        in_dir.add(path.replace(in_directory, ""))
    out_dir = set()
    for path, directories, files in os.walk(out_directory):
        out_dir.add(path.replace(out_directory, ""))
    assert in_dir == out_dir


def test_copy_directory_structure_with_skip(test_copy_directory_structure_fixture):
    in_directory, out_directory = test_copy_directory_structure_fixture
    skip_dirs = ["source", "subtitles"]
    copy_directory_structure(in_directory, out_directory, to_skip=skip_dirs)

    in_dir = set()
    for path, directories, files in os.walk(in_directory):
        if dont_skip_dir(skip_dirs, path):
            in_dir.add(path.replace(in_directory, ""))
    out_dir = set()
    for path, directories, files in os.walk(out_directory):
        out_dir.add(path.replace(out_directory, ""))
    assert in_dir == out_dir


def test_dont_skip_dir():
    assert dont_skip_dir([], "any string here will work") == True
    assert (
        dont_skip_dir(["Subtitles"], os.path.join("dir", "to", "not", "skip")) == True
    )
    assert (
        dont_skip_dir(["Subtitles"], os.path.join("dir", "to", "skip", "subtitles"))
        == False
    )
    assert (
        dont_skip_dir(["subtitles"], os.path.join("dir", "to", "skip", "Subtitles"))
        == False
    )
    assert (
        dont_skip_dir(["Subtitles"], os.path.join("dir", "to", "skip", "Subtitles"))
        == False
    )
    assert (
        dont_skip_dir(
            ["subtitles", "source"],
            "D:/Lightning videos/Szkolenia/M3 Supply chain/Szkolenie M3 Logistyka blok 1 - podstawy systemu\\Supply chain 1 - basics (pl).mp4",
        )
        == True
    )


def test_list_videos():
    videos = set(list_videos(IN_DIRECTORY))
    expected_videos = set(
        [
            os.path.join(IN_DIRECTORY, file)
            for file in [
                os.path.join("dir1", "test1"),
                os.path.join("dir2", "test2"),
                os.path.join("dir1", "subdir1_1", "test1_1"),
            ]
        ]
    )
    assert videos == expected_videos
