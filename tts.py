import sys

import numpy as np
import torch
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"
if device != "cuda":
    c = "_"
    while c not in "ynYN":
        c = input(
            "Failed to load CUDA, do You want to continue using CPU? (It will be extremely slow) [y/n]\n"
        ).strip()
        if c in "yY":
            break
        elif c in "nN":
            sys.exit()
model = "tts_models/en/multi-dataset/tortoise-v2"
tts = TTS(model).to(device)


def synthesize(
    text: str,
    *,
    speed: float = None,
    speaker: str = "myself",
    voice_dir: str = "voices/",
    **kwargs
) -> tuple[int, np.ndarray]:
    wav = tts.tts(
        text=text, voice_dir=voice_dir, speaker=speaker, speed=speed, **kwargs
    )
    sample_rate = 24000  # TODO: get from tts model
    if torch.is_tensor(wav):
        wav = wav.cpu().numpy()
    if isinstance(wav, list):
        wav = np.array(wav)

    return sample_rate, normalize(wav)


def normalize(wav: np.ndarray) -> np.ndarray:
    wav_norm = wav * (32767 / max(0.01, np.max(np.abs(wav))))
    return wav_norm.astype(np.int16)
