import os
import sys

main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_folder_path)

import tts
from voiceover import add_audio_to_video

in_file_path = os.path.join(main_folder_path, "tests", "test.mp4")
out_file_path = in_file_path.replace("test.mp4", "test-out.mp4")
segments = [
    {"text": "Good morning!", "start": 1.0, "end": 2.0},
    {"text": "Lisbon is beautiful", "start": 2.7, "end": 5.1},
]
MS = 1000
audios_with_timestamps = [
    (
        tts.synthesize(
            segment["text"],
            speed=1.2,
            voice_dir=os.path.join(main_folder_path, "voices"),
        ),
        int(segment["start"] * MS),
    )
    for segment in segments
]
add_audio_to_video(
    *zip(*audios_with_timestamps),
    in_file_path,
    out_file_path,
)
