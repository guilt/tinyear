"""Cheap offline acoustics. No cloud ASR. Words are a human field."""
from __future__ import annotations

import math
import struct
import wave
from pathlib import Path


def read_pcm16_bytes(blob: bytes) -> tuple[int, list[int]]:
    import io

    with wave.open(io.BytesIO(blob), "rb") as w:
        rate = w.getframerate()
        n = w.getnframes()
        width = w.getsampwidth()
        raw = w.readframes(n)
    if width != 2 or not raw:
        return rate, []
    samples = list(struct.unpack("<" + "h" * (len(raw) // 2), raw))
    return rate, samples


def read_pcm16(path: Path) -> tuple[int, list[int]]:
    return read_pcm16_bytes(Path(path).read_bytes())


def energy(samples: list[int]) -> float:
    if not samples:
        return 0.0
    return min(1.0, math.sqrt(sum(s * s for s in samples) / len(samples)) / 16000.0)


def zero_cross_hz(samples: list[int], rate: int) -> float:
    if len(samples) < 2:
        return 0.0
    zc = sum(1 for a, b in zip(samples, samples[1:]) if (a >= 0) != (b >= 0))
    return 0.5 * zc * rate / len(samples)


def duration_ms(n: int, rate: int) -> int:
    return int(1000 * n / max(rate, 1))


def peak(samples: list[int]) -> int:
    return max((abs(s) for s in samples), default=0)


def voiced(samples: list[int], rate: int) -> bool:
    return energy(samples) >= 0.02 and 60.0 <= zero_cross_hz(samples, rate) <= 800.0
