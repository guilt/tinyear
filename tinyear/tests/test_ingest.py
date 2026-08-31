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


def test_cli(tmp_path, monkeypatch):
    from tinyear.__main__ import main

    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.3)
    monkeypatch.setattr(
        "sys.argv",
        ["tinyear", "ingest", str(wav), "--out", str(tmp_path / "o"), "--transcript", "hi"],
    )
    assert main() == 0
