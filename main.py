import tts

import numpy as np

wav = tts.synthesize("THIS IS EXAMPLE TEXT")
print(np.shape(wav))