import os


import tts
from drive_io import copy_directory_structure, extract_mp3, list_videos
from subtitles import save_to_srt
from voice_recognition import transcribe_video
from voiceover import add_audio_to_video

IN_DIRECTORY = "videos/in/"
OUT_DIRECTORY = "videos/out/"
TEXT_KEYS = ["start", "end", "text"]
DIAG_KEYS = ["avg_logprob", "no_speech_prob"]

if __name__ == "__main__":
    copy_directory_structure(IN_DIRECTORY, OUT_DIRECTORY)
    for filename, extension in [file.split(".") for file in list_videos(IN_DIRECTORY)]:
        file_path = f"{filename}.{extension}"
        print(f"Transcribing {file_path}.{extension}")
        mp3 = extract_mp3(file_path)
        segments = transcribe_video(file_path)
        save_to_srt(segments, filename.replace(IN_DIRECTORY, OUT_DIRECTORY))
        MS = 1000
        audios_with_timestamps = [
            (tts.synthesize(segment["text"]), int(segment["start"] * MS))
            for segment in segments
        ]
        add_audio_to_video(
            *zip(*audios_with_timestamps),
            f"{filename}.mp4",
            filename.replace(IN_DIRECTORY, OUT_DIRECTORY),
        )
