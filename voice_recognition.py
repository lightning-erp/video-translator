from typing import Union

import numpy as np
import whisper

IN_DIRECTORY = "videos/in/"
OUT_DIRECTORY = "videos/out/"
TEXT_KEYS = ["start", "end", "text"]
DIAG_KEYS = ["avg_logprob", "no_speech_prob"]

voice_recognition = whisper.load_model("large")


def transcribe_video(
    video_filename: Union[str, np.ndarray]
) -> list[dict[str, Union[float, str]]]:
    """
    Returns list of dicts with the following structure:
        -- 'text' (str): Transcription of the segment,
        -- 'start' (float): start of the segment in seconds,
        -- 'end' (float): end of the segment in seconds.
    """
    segments: list[dict[str, Union[str, float]]] = voice_recognition.transcribe(
        video_filename, task="translate", language="pl"
    )["segments"]
    return [
        {key: value for key, value in segment.items() if key in TEXT_KEYS}
        for segment in segments
        if segment["text"].strip() != "..." and segment["text"].strip() != "."
    ]
