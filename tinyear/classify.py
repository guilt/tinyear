"""Cheap inventory classifier. No ASR. No weights.

Labels manner and nearest vowel atom. Words stay a human field.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

VOWEL_ATOMS = {
    "i": (310.0, 2565.0), "e": (610.0, 2061.0), "a": (840.0, 1221.0),
    "o": (655.0, 941.0), "u": (345.0, 974.0), "schwa": (575.0, 1680.0),
}
F1_BINS = [250, 350, 450, 550, 650, 750, 850, 950, 1100]
F2_BINS = [800, 950, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2600]

@dataclass
class EarClass:
    manner: str
    vowel: str
    place: str
    f1: float
    f2: float
    zcr_hz: float
    energy: float
    ok: bool
    note: str

def _goertzel_power(samples, rate, freq):
    if not samples:
        return 0.0
    w = 2.0 * math.pi * freq / rate
    coeff = 2.0 * math.cos(w)
    s0 = s1 = s2 = 0.0
    scale = 1.0 / 32768.0
    for x in samples:
        s0 = (x * scale) + coeff * s1 - s2
        s2 = s1
        s1 = s0
    return s1 * s1 + s2 * s2 - coeff * s1 * s2

def _peak_bin(samples, rate, bins):
    best_f, best_p = bins[0], -1.0
    for f in bins:
        p = _goertzel_power(samples, rate, float(f))
        if p > best_p:
            best_f, best_p = f, p
    return float(best_f), best_p

def _nearest_vowel(f1, f2):
    best, dist = "schwa", 1e18
    for name, (t1, t2) in VOWEL_ATOMS.items():
        d = ((f1 - t1) / 400.0) ** 2 + ((f2 - t2) / 800.0) ** 2
        if d < dist:
            best, dist = name, d
    return best, dist

def _energy(samples):
    if not samples:
        return 0.0
    return min(1.0, math.sqrt(sum(s * s for s in samples) / len(samples)) / 16000.0)

def _zcr(samples, rate):
    if len(samples) < 2:
        return 0.0
    zc = sum(1 for a, b in zip(samples, samples[1:]) if (a >= 0) != (b >= 0))
    return 0.5 * zc * rate / len(samples)

def classify_pcm(samples, rate=16000):
    from .acoustics import band_energy
    e = _energy(samples)
    z = _zcr(samples, rate)
    if e < 0.012:
        return EarClass("silence", "", "none", 0.0, 0.0, z, e, True, "quiet")
    f1, p1 = _peak_bin(samples, rate, F1_BINS)
    f2, p2 = _peak_bin(samples, rate, F2_BINS)
    vowel, dist = _nearest_vowel(f1, f2)
    low = band_energy(samples, rate, 200.0, 900.0)
    high = band_energy(samples, rate, 3000.0, 6000.0)
    tilt = high / max(low, 1e-9)
    place = "coronal" if f2 >= 1600 else ("labial" if f2 < 1100 else "velar")
    if tilt >= 2.2:
        kind = "fricative" if z >= 1400.0 else "stop"
        return EarClass(kind, "", place, f1, f2, z, e, True, f"tilt={tilt:.2f}")
    if tilt >= 1.6 and e >= 0.02 and z >= 1600.0:
        return EarClass("stop", "", place, f1, f2, z, e, True, f"tilt={tilt:.2f}")
    if p2 < p1 * 0.25 and e < 0.28 and f2 < 1200:
        nplace = "labial" if f2 < 1000 else "coronal"
        return EarClass("nasal", vowel, nplace, f1, f2, z, e, True, "damped-f2")
    return EarClass("vowel", vowel, "vowel", f1, f2, z, e, dist < 8.0, f"nn={dist:.2f}")

def classify_wav_bytes(blob):
    from .acoustics import read_pcm16_bytes
    rate, samples = read_pcm16_bytes(blob)
    return classify_pcm(samples, rate)
