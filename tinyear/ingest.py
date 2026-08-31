from __future__ import annotations
import math, struct, wave
from datetime import datetime, timezone
from pathlib import Path

def _pcm_energy(samples):
    if not samples: return 0.0
    return min(1.0, math.sqrt(sum(s * s for s in samples) / len(samples)) / 16000.0)

def _zero_cross_hz(samples, rate):
    if len(samples) < 2: return 0.0
    zc = sum(1 for a, b in zip(samples, samples[1:]) if (a >= 0) != (b >= 0))
    return 0.5 * zc * rate / len(samples)

def write_ear_pair(out_dir, stem, wav_src, transcript="", transcript_ok=None, source="desktop"):
    out_dir.mkdir(parents=True, exist_ok=True)
    dest_wav = out_dir / f"{stem}.ear.wav"
    if wav_src.resolve() != dest_wav.resolve():
        dest_wav.write_bytes(wav_src.read_bytes())
    with wave.open(str(wav_src), "rb") as w:
        rate, n, raw, width = w.getframerate(), w.getnframes(), w.readframes(w.getnframes()), w.getsampwidth()
        duration_ms = int(1000 * n / max(rate, 1))
    samples = list(struct.unpack("<" + "h" * (len(raw) // 2), raw)) if width == 2 else []
    if transcript_ok is None:
        transcript_ok = bool(transcript.strip())
    belief = transcript.strip() if transcript_ok else "I did not catch words."
    md = out_dir / f"{stem}.ear.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md.write_text("\n".join([
        "---", "modality: ear", f"time: {now}", f"source: {source}",
        f"duration_ms: {duration_ms}", "codec: wav", "confidence: 0.4",
        f"transcript_ok: {'true' if transcript_ok else 'false'}",
        f"transcript: {transcript.strip()}", "---", "", "## Belief", belief, "",
        "## Acoustics", f"pitch_mean_hz: {_zero_cross_hz(samples, rate):.1f}",
        f"energy: {_pcm_energy(samples):.2f}", "",
    ]), encoding="utf-8")
    return dest_wav, md

def ingest_wav(wav_path, out_dir, transcript="", stem=None):
    return write_ear_pair(out_dir, stem or wav_path.stem, wav_path, transcript=transcript)
