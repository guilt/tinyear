from __future__ import annotations
import math, struct, wave
from pathlib import Path

def write_tone_wav(path: Path, seconds: float = 1.2, sr: int = 16000) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = int(sr * seconds)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        frames = bytearray()
        for i in range(n):
            t = i / sr
            env = min(1.0, t * 8) * min(1.0, (seconds - t) * 6)
            sig = 0.35 * math.sin(2 * math.pi * 220 * t) + 0.2 * math.sin(2 * math.pi * 880 * t) + 0.08 * math.sin(2 * math.pi * 2400 * t)
            frames += struct.pack("<h", int(max(-1, min(1, sig * env)) * 20000))
        w.writeframes(frames)
    return path
