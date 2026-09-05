from pathlib import Path
from tinyear.fixtures import write_tone_wav
dest = Path(__file__).resolve().parent / "sample.wav"
write_tone_wav(dest)
print(dest)
