import logging
import os

logging.basicConfig(
    filename="log.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logging.info("Begin loading imports")

import tts
from drive_io import extract_mp3, list_videos
from subtitles import save_to_srt
from voice_recognition import transcribe_video
from voiceover import add_audio_to_video

logging.info("Done loading imports")

IN_DIRECTORY = "videos/in/"
OUT_DIRECTORY = "videos/out/"
TEXT_KEYS = ["start", "end", "text"]
DIAG_KEYS = ["avg_logprob", "no_speech_prob"]

if __name__ == "__main__":
    logging.info("Begin loop")
    for filename, extension in [file.split(".") for file in list_videos(IN_DIRECTORY)]:
        file_path = f"{filename}.{extension}"
        logging.info(f"Begin transcribing {file_path}")
        print(f"Transcribing {file_path}")
        logging.debug("Begin extract mp3")
        mp3 = extract_mp3(file_path)
        logging.debug("End extracting mp3")
        logging.debug("Begin transcribing video")
        segments = transcribe_video(file_path)
        logging.debug("End transcriging video")
        logging.debug("Begin saving transcription to .srt")
        save_to_srt(segments, os.path.join(OUT_DIRECTORY, filename))
        logging.debug("End saving transctiption to .srt")
        logging.debug("Begin generating audio with timestamps")
        audios_with_timestamps = [
            (tts.synthesize(segment["text"]), int(segment["start"] * 1000))
            for segment in segments
        ]
        logging.debug("End generating audio with timestamps")
        fs = audios_with_timestamps[0][0]
        logging.debug(f"fs correctly loaded (fs={fs})")
        logging.debug("Begin adding audio to video")
        add_audio_to_video(
            *zip(*audios_with_timestamps),
            f"{filename}.mp4",
            os.path.join(OUT_DIRECTORY, f"{filename}.{extension}"),
            sample_rate=fs,
        )
        logging.debug("End adding audio to video")
        logging.info(f"Finished transcribing {file_path}")
