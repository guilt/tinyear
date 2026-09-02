# TinyEar

Short clip + sidecar. Honest when words fail.

```bash
python -m pip install -e ".[dev]"
make tests
tinyear ingest examples/sample.wav --out memory/ --transcript "set a timer"
```

Empty transcript → `I did not catch words.`

`tinyear.classify` labels manner + nearest vowel atom (Goertzel + tilt).
Sidecar: `class_manner`, `class_vowel`, `class_place`, `class_ok`.

C twin (ESP32-S3): https://github.com/guilt/TinyEar-C
