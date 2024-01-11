# Training Video Translation and Voiceover

Training Video Translation and Voiceover tool based on OpenAI's Whisper for voice recognition, TortoiseTTS for generating text-to-speech and FFmpeg with PyDub for adding the new voice to the existing video. Generates subtitles using PySrt.


## Installation

1. Clone the repository.
2. Remember to [create](https://docs.python.org/3/library/venv.html#creating-virtual-environments) and activate the virtual environment by running:
    * Windows (using powershell): `path/to/venv/scripts/activate.ps1`
    * Linux: `source path/to/venv/bin/activate`
3. Instll the requirements: `pip install -r requirements.txt`.
4. Install PyTorch according to [PyTorch installation guide](https://pytorch.org/get-started/locally/). Make sure to already have [CUDA drivers](https://developer.nvidia.com/cuda-downloads) installed, otherwise text-to-speech synthesis is too slow.


## Usage

1. Specify `IN_DIRECTORY`, `OUT_DIRECTORY` and `DIRS_TO_SKIP` (directories containing specified substrings will be skipped).
2. Activate the virtual environment:
    * Windows (using powershell): `path/to/venv/sctipts/activate`
    * Linux: `source /path/to/venv/bin/activate`
3. Set parameters in `main.py`:
    * `IN_DIRECTORY` - directory containing input .mp4 files
    * `OUT_DIRECTORY` - directory containing output .mp4 files
    * `TTS_SIZE` - size of Whisper model, for available models check [OpenAI's Whisper GitHub README](https://github.com/openai/whisper#available-models-and-languages)
    * `TTS_SPEED` - speed of synthesised speech (detaulf: 1.0). Going far away from 1 is not recommended.
    * `DIRS_TO_SKIP` - directories containing substrings lised in this variable will not be processed (optional, `[]` to process all directories)
    * `LANGUAGE` - language of the input video (optional, `None` to not specify)
    * `TASK` - task that OpenAI's Whisper is supposed to perform (optional, `None` to not specify)
    * `INPUT_LANGUAGE_INDICATOR` - part of filename to replace (optional, `""` to not replace)
    * `OUTPUT_LANGUAGE_INDICATOR` - string to replace with (optional, `""` to not replace)
4. Run `py main.py`.
