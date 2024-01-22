import logging
import os
from datetime import timedelta
from time import perf_counter

import tts
from drive_io import copy_directory_structure, dont_skip_dir, list_videos
from subtitles import save_to_srt
from text_processing import (
    merge_repeats,
    merge_on_interpunction,
    split_on_interpunction,
)
from voice_recognition import VoiceRecognition
from voiceover import add_audio_to_video

logging.basicConfig(
    filename="times.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(message)s",
)

IN_DIRECTORY = "D:/Lightning videos/Szkolenia/M3 Supply chain"
OUT_DIRECTORY = "D:/Lightning videos/Trainings/M3 Supply chain"
DIRS_TO_SKIP = [
    "subtitles",
    "source",
    "Szkolenie M3 Logistyka blok 2 - Podstawowe dane",
]
TTS_SPEED = 1.2
WHISPER_SIZE = "large"
LANGUAGE = "pl"
TASK = "translate"
INPUT_LANGUAGE_INDICATOR = "(pl)"
OUTPUT_LANGUAGE_INDICATOR = "(en)"


if __name__ == "__main__":
    try:
        logging.info("Loading voice recognition model")
        whisper = VoiceRecognition(WHISPER_SIZE)
        logging.info("Beginning translation process")
        copy_directory_structure(IN_DIRECTORY, OUT_DIRECTORY, to_skip=DIRS_TO_SKIP)
        logging.info("Directory structure copied")
        files = [
            file
            for file in list_videos(IN_DIRECTORY)
            if ".mp4" in file and dont_skip_dir(DIRS_TO_SKIP, file)
        ]
        logging.info(f"Detected {len(files)} to translate")
        for file in files:
            start = perf_counter()
            filename, extension = os.path.splitext(file)
            in_file_path = f"{filename}{extension}"
            out_file_path = f"{filename}{extension}".replace(
                IN_DIRECTORY, OUT_DIRECTORY
            ).replace(INPUT_LANGUAGE_INDICATOR, OUTPUT_LANGUAGE_INDICATOR)
            logging.info(f"Transcribing {in_file_path}")
            logging.info(f"Output will be in {out_file_path}")
            if os.path.isfile(f"{out_file_path}"):
                print(f"{out_file_path} already exists, skipping file")
                logging.info(f"{out_file_path} already exists, skipping file")
                continue
            logging.info("Beggining video transcription")
            segments = merge_on_interpunction(
                merge_repeats(
                    whisper.transcribe_video(in_file_path, language=LANGUAGE, task=TASK)
                )
            )
            logging.info("Beggining .srt generation")
            save_to_srt(
                segments,
                filename.replace(IN_DIRECTORY, OUT_DIRECTORY).replace(
                    INPUT_LANGUAGE_INDICATOR, OUTPUT_LANGUAGE_INDICATOR
                ),
            )
            logging.info("Beggining text-to-speech generation")
            MS = 1000
            audios_with_timestamps = [
                (
                    tts.synthesize(segment["text"], speed=TTS_SPEED),
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
                print("No speech detected")

    except Exception as e:
        logging.error(f"Exception occured: {e}")
