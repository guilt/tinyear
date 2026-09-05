from tinyear.acoustics import read_pcm16_bytes
from tinyear.classify import classify_pcm
from tinyear.ingest import MISS, write_ear_pair

def _try_howl():
    try:
        from tinyhowl.inventory import render_primitive
        from tinyhowl.synth import wav_bytes
    except ImportError:
        return None
    return render_primitive, wav_bytes

def test_silence_is_silence():
    cls = classify_pcm([0] * 1600, 16000)
    assert cls.manner == "silence" and cls.ok

def test_inventory_roundtrip(tmp_path):
    helper = _try_howl()
    if helper is None:
        return
    render_primitive, wav_bytes = helper
    close = {"i": {"i", "e"}, "e": {"e", "i", "schwa"}, "a": {"a", "o", "schwa"},
             "o": {"o", "u", "a"}, "u": {"u", "o"}, "schwa": {"schwa", "e", "a"}}
    for name, allowed in close.items():
        cls = classify_pcm(list(render_primitive(name)), 16000)
        assert cls.manner == "vowel", (name, cls)
        assert cls.vowel in allowed, (name, cls)
    for name in ("s", "sh", "f"):
        cls = classify_pcm(list(render_primitive(name)), 16000)
        assert cls.manner in {"fricative", "stop", "unknown"}, (name, cls)
    blob = wav_bytes(render_primitive("a"))
    wav = tmp_path / "a.wav"
    wav.write_bytes(blob)
    _, md = write_ear_pair(tmp_path, "a", wav)
    assert "class_manner:" in md.read_text(encoding="utf-8")
    assert MISS in md.read_text(encoding="utf-8")
    rate, samples = read_pcm16_bytes(blob)
    assert rate == 16000 and samples
