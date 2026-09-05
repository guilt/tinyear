from __future__ import annotations

import math
import struct
import wave
from pathlib import Path


def write_tone_wav(path: Path, seconds: float = 1.2, sr: int = 16000, f0: float = 220.0) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    n = int(sr * seconds)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        frames = bytearray()
        for i in range(n):
            t = i / sr
            env = min(1.0, t * 8) * min(1.0, (seconds - t) * 6)
            sig = (
                0.35 * math.sin(2 * math.pi * f0 * t)
                + 0.2 * math.sin(2 * math.pi * f0 * 4 * t)
                + 0.08 * math.sin(2 * math.pi * 2400 * t)
            )
            frames += struct.pack("<h", int(max(-1, min(1, sig * env)) * 20000))
        w.writeframes(frames)
    return path


def write_silence_wav(path: Path, seconds: float = 0.4, sr: int = 16000) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    n = int(sr * seconds)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"\x00\x00" * n)
    return path
