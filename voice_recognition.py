from typing import Union

import numpy as np
import whisper

TEXT_KEYS = ["start", "end", "text"]
DIAG_KEYS = ["avg_logprob", "no_speech_prob"]


class VoiceRecognition:
    def __init__(self, model_size: str):
        self.model = whisper.load_model(model_size)

    def transcribe_video(
        self,
        video_filename: Union[str, np.ndarray],
        *,
        language: str,
        task: str,
    ) -> list[dict[str, Union[float, str]]]:
        """
        Returns list of dicts with the following structure:
            -- 'text' (str): Transcription of the segment,
            -- 'start' (float): start of the segment in seconds,
            -- 'end' (float): end of the segment in seconds.
        """
        segments: list[dict[str, Union[str, float]]] = self.model.transcribe(
            video_filename, task=task, language=language
        )["segments"]
        return [
            {key: value for key, value in segment.items() if key in TEXT_KEYS}
            for segment in segments
            if segment["text"].strip() != "..." and segment["text"].strip() != "."
        ]
