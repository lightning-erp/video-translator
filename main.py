import logging
import os
import sys
from datetime import timedelta
from time import perf_counter
from typing import Literal

import torch
from PyQt6.QtWidgets import QApplication

from drive_io import copy_directory_structure, dont_skip_dir, list_videos
from gui import MainWindow
from subtitles import save_to_srt
from text_processing import merge_on_interpunction, merge_repeats
from tts import TextToSpeech
from voice_recognition import VoiceRecognition
from voiceover import add_audio_to_video

logging.basicConfig(
    filename="times.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(message)s",
)

# IN_DIRECTORY = "D:/Lightning videos/Szkolenia/M3 Supply chain"
# OUT_DIRECTORY = "D:/Lightning videos/Trainings/M3 Supply chain"
# DIRS_TO_SKIP = [
#     "subtitles",
#     "source",
# ]
# TTS_SPEED = 1.2
# WHISPER_SIZE = "large"
# LANGUAGE = "pl"
# TASK = "translate"
# INPUT_LANGUAGE_INDICATOR = "(pl)"
# OUTPUT_LANGUAGE_INDICATOR = "(en)"


def start_translation_and_voiceover(
    in_directory: str,
    out_directory: str,
    dirs_to_skip: list[str],
    tts_speed: float,
    whisper_size: Literal["tiny", "base", "small", "medium", "large"],
    language: str,
    input_language_indicator: str,
    output_language_indicator: str,
    device: Literal["cuda", "cpu"],
):
    logging.info("Loading voice recognition model")
    whisper = VoiceRecognition(whisper_size)
    logging.info("Loading text-to-speech model")
    tts = TextToSpeech(device)
    logging.info("Beginning translation process")
    copy_directory_structure(in_directory, out_directory, to_skip=dirs_to_skip)
    logging.info("Directory structure copied")
    files = [
        file
        for file in list_videos(in_directory)
        if ".mp4" in file and dont_skip_dir(dirs_to_skip, file)
    ]
    logging.info(f"Detected {len(files)} to translate")
    for file in files:
        start = perf_counter()
        filename, extension = os.path.splitext(file)
        in_file_path = f"{filename}{extension}"
        out_file_path = f"{filename}{extension}".replace(
            in_directory, out_directory
        ).replace(input_language_indicator, output_language_indicator)
        logging.info(f"Transcribing {in_file_path}")
        logging.info(f"Output will be in {out_file_path}")
        if os.path.isfile(f"{out_file_path}"):
            logging.info(f"{out_file_path} already exists, skipping file")
            continue
        logging.info("Beggining video transcription")
        segments = merge_on_interpunction(
            merge_repeats(
                whisper.transcribe_video(
                    in_file_path, language=language, task="translate"
                )
            )
        )

        logging.info("Beggining .srt generation")
        save_to_srt(
            segments,
            filename.replace(in_directory, out_directory).replace(
                input_language_indicator, output_language_indicator
            ),
        )
        logging.info("Beggining text-to-speech generation")
        MS = 1000
        audios_with_timestamps = [
            (
                tts.synthesize(segment["text"], speed=tts_speed),
                int(segment["start"] * MS),
            )
            for segment in segments
        ]
        logging.info("Beggining adding audio to video")
        if audios_with_timestamps:
            video_length = add_audio_to_video(
                *zip(*audios_with_timestamps),
                in_file_path,
                out_file_path,
            )
            end = perf_counter()
            logging.info(
                f"Translation and voiceover for {out_file_path} [{str(timedelta(milliseconds=video_length))}] took {str(timedelta(seconds=end-start))}"
            )
        else:
            logging.info(f"No speech detected in {in_file_path}.")


def main():
    import time

    start = time.perf_counter()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    app = QApplication(sys.argv)
    window = MainWindow(
        start_translation_and_voiceover,
        VoiceRecognition.supported_languages,
        device,
    )
    print(time.perf_counter() - start)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
