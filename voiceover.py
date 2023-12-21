from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip

TORTOISE_SAMPLERATE = 24000

with VideoFileClip("test.mp4", audio=False) as video:
    import tts
    audio = AudioFileClip(tts.synthesize("Extremely silly, full time goofy ioioio shenanigans"), fps=TORTOISE_SAMPLERATE)
    video.set_audio(audio)
    video.write_videofile("test-out.mp4")
