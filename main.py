import tts
from voiceover import add_audio_to_video

wav1, sr = tts.synthesize("THIS IS EXAMPLE TEXT")
wav2, sr = tts.synthesize("AGAIN SOME RANDOM SHIT")
add_audio_to_video(
    [wav1, wav2], [1000, 4000], "test.mp4", "test-out-main.mp4", sample_rate=sr
)
