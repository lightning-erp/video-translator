import os

# import tts
from drive_io import copy_directory_structure, extract_mp3, list_videos, dont_skip_dir
from subtitles import save_to_srt
from voice_recognition import transcribe_video
from voiceover import add_audio_to_video

IN_DIRECTORY = "D:/Lightning videos/Szkolenia/M3 Supply chain/"
OUT_DIRECTORY = "D:/Lightning videos/Trainings/M3 Supply chain/"
DIRS_TO_SKIP = ["subtitles", "source"]
TEXT_KEYS = ["start", "end", "text"]
DIAG_KEYS = ["avg_logprob", "no_speech_prob"]

if __name__ == "__main__":
    copy_directory_structure(IN_DIRECTORY, OUT_DIRECTORY, to_skip=DIRS_TO_SKIP)
    files = [
        (file, dont_skip_dir(DIRS_TO_SKIP, file))
        for file in list_videos(IN_DIRECTORY)
        if ".mp4" in file  # and dont_skip_dir(DIRS_TO_SKIP, file)
    ]
    print(files)
    files = [file for file in list_videos(IN_DIRECTORY) if ".mp4" in file]
    print(files)
    for file in files:
        filename, extension = file.split(".")
        in_file_path = f"{filename}.{extension}"
        out_file_path = f"{filename}.{extension}".replace(
            IN_DIRECTORY, OUT_DIRECTORY
        ).replace("(pl)", "(en)")
        print(f"Transcribing {in_file_path}")
        print(f"Output will be in {out_file_path}")
        if os.path.isfile(f"{out_file_path}"):
            print(f"{out_file_path} already exists, skipping file")
            continue
        raise ValueError
        mp3 = extract_mp3(in_file_path)
        segments = transcribe_video(in_file_path)
        save_to_srt(
            segments,
            filename.replace(IN_DIRECTORY, OUT_DIRECTORY).replace("(pl)", "(en)"),
        )
        MS = 1000
        audios_with_timestamps = [
            (tts.synthesize(segment["text"], speed=1.2), int(segment["start"] * MS))
            for segment in segments
        ]
        add_audio_to_video(
            *zip(*audios_with_timestamps),
            in_file_path,
            out_file_path,
        )
