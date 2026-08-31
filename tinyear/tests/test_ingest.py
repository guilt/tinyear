from pathlib import Path
from tinyear.fixtures import write_tone_wav
from tinyear.ingest import ingest_wav

def test_transcript_ok(tmp_path: Path):
    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.5)
    dest, md = ingest_wav(wav, tmp_path / "out", transcript="set a timer")
    text = md.read_text(encoding="utf-8")
    assert "transcript_ok: true" in text and "set a timer" in text and dest.exists()

def test_honest_miss(tmp_path: Path):
    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.4)
    _, md = ingest_wav(wav, tmp_path / "out")
    text = md.read_text(encoding="utf-8")
    assert "transcript_ok: false" in text and "I did not catch words." in text

def test_acoustics_present(tmp_path: Path):
    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.6)
    _, md = ingest_wav(wav, tmp_path / "out", transcript="hi")
    text = md.read_text(encoding="utf-8")
    assert "pitch_mean_hz:" in text and "energy:" in text

def test_cli(tmp_path, monkeypatch):
    from tinyear.__main__ import main
    wav = write_tone_wav(tmp_path / "s.wav", seconds=0.3)
    monkeypatch.setattr("sys.argv", ["tinyear", "ingest", str(wav), "--out", str(tmp_path / "o"), "--transcript", "hi"])
    assert main() == 0
