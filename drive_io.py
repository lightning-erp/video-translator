import io
import os

import librosa
import numpy as np
from pydub import AudioSegment


def list_videos(directory: str) -> list[str]:
    videos = list()
    for path, directories, files in os.walk(directory):
        videos.extend([os.path.join(path, file) for file in files])

    return videos


def copy_directory_structure(
    in_directory: str, out_directory: str, *, to_skip: list[str] = []
):
    for path, directories, files in os.walk(in_directory):
        for dir in [directory for directory in directories]:
            try:
                new_dir = os.path.join(path.replace(in_directory, out_directory), dir)
                if dont_skip_dir(to_skip, new_dir):
                    os.makedirs(new_dir)
            except FileExistsError:
                pass


def dont_skip_dir(to_skip, target_dir):
    return all([dir.lower() not in target_dir.lower() for dir in to_skip])


def extract_mp3(mp4_path: str) -> np.ndarray:
    audio: AudioSegment = AudioSegment.from_file(mp4_path, "mp4")
    buffer = io.BytesIO()
    audio.export(buffer, format="mp3")
    buffer.seek(0)
    mp3, fs = librosa.load(buffer, sr=None)
    return fs, mp3
