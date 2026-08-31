"""Offline ear corpus: 6 tones + 1 silence. No network, no ASR."""
from pathlib import Path

from tinyear.fixtures import write_silence_wav, write_tone_wav
from tinyear.ingest import ingest_wav

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out" / "corpus"
VOWELS = [("aa", 730), ("ee", 270), ("oo", 300), ("eh", 610), ("uh", 500), ("ih", 390)]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, f0 in VOWELS:
        wav = write_tone_wav(OUT / f"{name}.wav", seconds=0.6, f0=f0)
        ingest_wav(wav, OUT, transcript="", stem=name)
    silent = write_silence_wav(OUT / "silence.wav", seconds=0.4)
    ingest_wav(silent, OUT, transcript="", stem="silence")
    print(OUT)
    for md in sorted(OUT.glob("*.ear.md")):
        print(" ", md.name)


if __name__ == "__main__":
    main()
