from typing import Literal

import numpy as np
import torch
from TTS.api import TTS

from text_processing import split_acronyms


class TextToSpeech:
    def __init__(
        self,
        device: Literal["cuda", "cpu"],
        model="tts_models/en/multi-dataset/tortoise-v2",
    ):
        self.device = device
        self.model = model
        self.tts = TTS(model).to(device)

    def synthesize(
        self,
        text: str,
        *,
        speed: float = None,
        speaker: str = "myself",
        voice_dir: str = "voices/",
        **kwargs
    ) -> tuple[int, np.ndarray]:
        wav = self.tts.tts(
            text=split_acronyms(text),
            voice_dir=voice_dir,
            speaker=speaker,
            speed=speed,
            **kwargs
        )
        sample_rate = 24000  # TODO: get from tts model
        if torch.is_tensor(wav):
            wav = wav.cpu().numpy()
        if isinstance(wav, list):
            wav = np.array(wav)

        return sample_rate, self.normalize(wav)

    def normalize(self, wav: np.ndarray) -> np.ndarray:
        wav_norm = wav * (32767 / max(0.01, np.max(np.abs(wav))))
        return wav_norm.astype(np.int16)
