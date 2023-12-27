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
            return None
    except ffmpeg.Error as e:
        print(e)
        return None


def load_wav_to_buffer(base_audio):
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
    ffmpeg.output(
        video.video,
        audio,
        out_video_filename,
        vcodec="copy",
        acodec="aac",
        map="[aout]",
        filter_complex=filter_complex,
    ).run(input=audio_bytes.read())


# if __name__ == "__main__":
#     import tts

#     VIDEO_PATH = "test.mp4"
#     TEXT1, TEXT1_TIMESTAMP = "Extremely silly, full time goofy. shenanigans.", 1000
#     TEXT2, TEXT2_TIMESTAMP = "undoubtedly", 7500

#     audio1, sr = tts.synthesize(TEXT1)
#     audio2, sr = tts.synthesize(TEXT2)

#     audio1 = numpy_to_pydub_audiosegment(audio1, sr)
#     audio2 = numpy_to_pydub_audiosegment(audio2, sr)

#     video_length = get_video_length(VIDEO_PATH)
#     audio = AudioSegment.silent(duration=video_length)
#     print(f"video length: {video_length}")

#     for segment, timestamp in zip([audio1, audio2], [TEXT1_TIMESTAMP, TEXT2_TIMESTAMP]):
#         audio = audio.overlay(segment, position=timestamp)

#     audio_bytes = BytesIO()
#     audio.export(audio_bytes, format="wav")
#     audio_bytes.seek(0)

#     video = ffmpeg.input(VIDEO_PATH)
#     audio = ffmpeg.input("pipe:0", format="wav", thread_queue_size=512)
#     filter_complex = "[0:a][1:a]amix=inputs=2:duration=longest[aout]"
#     ffmpeg.output(
#         video.video,
#         audio,
#         "test-out2.mp4",
#         vcodec="copy",
#         acodec="aac",
#         map="[aout]",
#         **{"filter_complex": filter_complex},
#     ).run(input=audio_bytes.read())
