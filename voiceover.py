import os
from io import BytesIO
from typing import Union

import ffmpeg
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile


def numpy_to_pydub_audiosegment(input: np.ndarray, sample_rate: int) -> AudioSegment:
    input = input.astype(np.int16)
    buffer = BytesIO()
    wavfile.write(buffer, sample_rate, input)
    buffer.seek(0)
    audio_segment = AudioSegment.from_wav(buffer)
    return audio_segment


def get_video_length(filename: str) -> Union[int, None]:
    """Returns the video length in miliseconds."""
    try:
        probe = ffmpeg.probe(filename)
        video_streams = [
            stream for stream in probe["streams"] if stream["codec_type"] == "video"
        ]
        if video_streams:
            duration = int(float(video_streams[0]["duration"]) * 1000)
            return duration
        else:
            print(f"No video stream found in file {filename}.")
            return 0
    except ffmpeg.Error as e:
        print(e)
        return None


def load_wav_to_buffer(base_audio) -> BytesIO:
    audio_bytes = BytesIO()
    base_audio.export(audio_bytes, format="wav")
    audio_bytes.seek(0)
    return audio_bytes


def add_audio_to_video(
    audios: list[np.ndarray],
    timestamps: list[int],
    in_video_filename: str,
    out_video_filename: str = "out.mp4",
    *,
    sample_rate: int = 24000,
) -> None:
    assert len(audios) == len(timestamps)
    video_length = get_video_length(in_video_filename)
    base_audio = AudioSegment.silent(duration=video_length)
    for audio, timestamp in zip(audios, timestamps):
        audio = numpy_to_pydub_audiosegment(audio, sample_rate)
        base_audio = base_audio.overlay(audio, position=timestamp)
    audio_bytes = load_wav_to_buffer(base_audio)
    video = ffmpeg.input(in_video_filename)
    audio = ffmpeg.input("pipe:0", format="wav", thread_queue_size=512)
    filter_complex = "[0:a][1:a]amix=inputs=2:duration=longest[aout]"
    path = out_video_filename.split(".")[0]
    if not os.path.isdir(path):
        os.mkdir(path)
    ffmpeg.output(
        video.video,
        audio,
        out_video_filename,
        vcodec="copy",
        acodec="aac",
        map="[aout]",
        filter_complex=filter_complex,
    ).run(input=audio_bytes.read())
    print(f"Video with overlaid audio saved to {out_video_filename}")
