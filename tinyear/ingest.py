from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .acoustics import duration_ms, energy, read_pcm16, zero_cross_hz


MISS = "I did not catch words."


def write_ear_pair(out_dir, stem, wav_src, transcript="", transcript_ok=None, source="desktop"):
    out_dir = Path(out_dir)
    wav_src = Path(wav_src)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest_wav = out_dir / f"{stem}.ear.wav"
    if wav_src.resolve() != dest_wav.resolve():
        dest_wav.write_bytes(wav_src.read_bytes())
    rate, samples = read_pcm16(wav_src)
    dur = duration_ms(len(samples), rate)
    if transcript_ok is None:
        transcript_ok = bool(str(transcript).strip())
    belief = str(transcript).strip() if transcript_ok else MISS
    md = out_dir / f"{stem}.ear.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md.write_text(
        "\n".join(
            [
                "---",
                "modality: ear",
                f"time: {now}",
                f"source: {source}",
                f"duration_ms: {dur}",
                "codec: wav",
                "confidence: 0.4",
                f"transcript_ok: {'true' if transcript_ok else 'false'}",
                f"transcript: {str(transcript).strip()}",
                "---",
                "",
                "## Belief",
                belief,
                "",
                "## Acoustics",
                f"pitch_mean_hz: {zero_cross_hz(samples, rate):.1f}",
                f"energy: {energy(samples):.2f}",
                f"samples: {len(samples)}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return dest_wav, md


def ingest_wav(wav_path, out_dir, transcript="", stem=None, source="desktop"):
    wav_path = Path(wav_path)
    return write_ear_pair(
        out_dir,
        stem or wav_path.stem,
        wav_path,
        transcript=transcript,
        source=source,
    )


def ingest_bytes(blob: bytes, out_dir, stem: str, transcript="", source="pipe"):
    """Ingest a WAV blob (stdin / process pipe). Writes the pair to disk."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"{stem}.ear.wav"
    dest.write_bytes(blob)
    return write_ear_pair(out_dir, stem, dest, transcript=transcript, source=source)
