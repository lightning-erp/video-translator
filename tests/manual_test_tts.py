import os
import sys

main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_folder_path)

import tts

x = tts.synthesize("good morning", speed=1.2)
