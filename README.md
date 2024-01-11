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
3. Run `py main.py`
