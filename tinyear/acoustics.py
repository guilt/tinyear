"""Cheap offline acoustics. No cloud ASR. Words are a human field."""
from __future__ import annotations

import math
import struct
import wave
from pathlib import Path


def read_pcm16_bytes(blob: bytes):
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


def read_pcm16(path: Path):
    return read_pcm16_bytes(Path(path).read_bytes())


def energy(samples):
    if not samples:
        return 0.0
    return min(1.0, math.sqrt(sum(s * s for s in samples) / len(samples)) / 16000.0)


def zero_cross_hz(samples, rate):
    if len(samples) < 2:
        return 0.0
    zc = sum(1 for a, b in zip(samples, samples[1:]) if (a >= 0) != (b >= 0))
    return 0.5 * zc * rate / len(samples)


def duration_ms(n, rate):
    return int(1000 * n / max(rate, 1))


def peak(samples):
    return max((abs(s) for s in samples), default=0)


def band_energy(samples, rate, lo, hi):
    if not samples or rate <= 0:
        return 0.0
    mid = (lo + hi) / 2.0
    acc = 0.0
    scale = 1.0 / 32768.0
    for freq in (lo, mid, hi):
        w = 2.0 * math.pi * freq / rate
        coeff = 2.0 * math.cos(w)
        s0 = s1 = s2 = 0.0
        for x in samples:
            s0 = x * scale + coeff * s1 - s2
            s2 = s1
            s1 = s0
        acc += s1 * s1 + s2 * s2 - coeff * s1 * s2
    return acc / 3.0


def pitch_hz(samples, rate, lo=120.0, hi=900.0):
    if len(samples) < rate // 20:
        return 0.0
    n = len(samples)
    a = n // 5
    b = min(n, a + rate // 2)
    win = samples[a:b] or samples
    lag_lo = max(2, int(rate / hi))
    lag_hi = min(len(win) - 2, int(rate / lo))
    if lag_hi <= lag_lo:
        return 0.0
    best_lag, best = lag_lo, -1e18
    for lag in range(lag_lo, lag_hi + 1):
        acc = 0.0
        count = len(win) - lag
        step = 2 if count > 400 else 1
        for i in range(0, count, step):
            acc += win[i] * win[i + lag]
        if acc > best:
            best, best_lag = acc, lag
    return rate / best_lag if best > 0 else 0.0


def voiced(samples, rate):
    if energy(samples) < 0.02:
        return False
    f0 = pitch_hz(samples, rate)
    return 80.0 <= f0 <= 1000.0
