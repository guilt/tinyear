# TinyEar

Tiny is a markdown cache that can grow ears, a mouth, and borrowed eyes. If a sense is missing it says so. Port 11434. Files you can delete.

**Job:** short clip + sidecar. Honest when words fail. Ear can stay off and Tiny is still complete.

```bash
python -m pip install -e ".[dev]"
make tests
make examples
tinyear ingest examples/sample.wav --out memory/ --transcript "set a timer"
```

Empty transcript → `transcript_ok: false` and belief = `I did not catch words.`

Tests use a generated 16 kHz formant tone so they run offline.
`make examples` also writes a 6-vowel + silence corpus under `examples/out/corpus/`.

Optional real speech: `python scripts/fetch_speech.py` prints how to pull
LibriSpeech dev-clean from OpenSLR. TinyEar will not caption it for you.
