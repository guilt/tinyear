from pathlib import Path

from tinyear.acoustics import energy, voiced
from tinyear.fixtures import write_silence_wav, write_tone_wav
from tinyear.ingest import MISS, ingest_wav
from tinyear.sidecar import parse_ear


def test_transcript_ok(tmp_path: Path):
    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.5)
    dest, md = ingest_wav(wav, tmp_path / "out", transcript="set a timer")
    text = md.read_text(encoding="utf-8")
    assert "transcript_ok: true" in text and "set a timer" in text and dest.exists()


def test_honest_miss(tmp_path: Path):
    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.4)
    _, md = ingest_wav(wav, tmp_path / "out")
    text = md.read_text(encoding="utf-8")
    assert "transcript_ok: false" in text and MISS in text


def test_acoustics_present(tmp_path: Path):
    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.6)
    _, md = ingest_wav(wav, tmp_path / "out", transcript="hi")
    text = md.read_text(encoding="utf-8")
    assert "pitch_mean_hz:" in text and "energy:" in text


def test_parse_roundtrip(tmp_path: Path):
    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.3)
    _, md = ingest_wav(wav, tmp_path / "out", transcript="hello")
    sc = parse_ear(md)
    assert sc.transcript_ok is True
    assert sc.belief == "hello"
    assert sc.wav_path and Path(sc.wav_path).exists()


def test_silence_not_voiced(tmp_path: Path):
    wav = write_silence_wav(tmp_path / "z.wav")
    from tinyear.acoustics import read_pcm16

    rate, samples = read_pcm16(wav)
    assert energy(samples) == 0.0
    assert voiced(samples, rate) is False


def test_cli(tmp_path):
    from tinyear.__main__ import main

    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.3)
    assert main(["ingest", str(wav), "--out", str(tmp_path / "o"), "--transcript", "hi"]) == 0


def test_ingest_bytes_and_stdin_cli(tmp_path):
    import os
    import subprocess
    import sys

    from tinyear.ingest import ingest_bytes

    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.3)
    blob = wav.read_bytes()
    dest, md = ingest_bytes(blob, tmp_path / "b", "pipe")
    assert dest.exists() and "transcript_ok: false" in md.read_text(encoding="utf-8")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2]) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-m", "tinyear", "ingest", "-", "--out", str(tmp_path / "s"), "--stem", "stdin"],
        input=blob,
        env=env,
        cwd=str(Path(__file__).resolve().parents[2]),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=15,
    )
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    assert (tmp_path / "s" / "stdin.ear.md").exists()
