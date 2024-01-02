import os
import shutil
import sys

import pytest

main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_folder_path)

from drive_io import copy_directory_structure, list_videos

IN_DIRECTORY = os.path.join(main_folder_path, "tests", "directories_test_dir", "in")
OUT_DIRECTORY = os.path.join(main_folder_path, "tests", "directories_test_dir", "out")


@pytest.fixture
def test_copy_directory_structure_fixture():
    yield IN_DIRECTORY, OUT_DIRECTORY

    shutil.rmtree(OUT_DIRECTORY)


def test_copy_directory_structure(test_copy_directory_structure_fixture):
    in_directory, out_directory = test_copy_directory_structure_fixture
    copy_directory_structure(in_directory, out_directory)

    in_dir = set()
    for path, directories, files in os.walk(in_directory):
        in_dir.add(path.replace(in_directory, ""))
    out_dir = set()
    for path, directories, files in os.walk(out_directory):
        out_dir.add(path.replace(out_directory, ""))
    print(in_dir, out_dir)
    assert in_dir == out_dir


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
