# TinyEar

Tiny is a markdown cache that can grow ears, a mouth, and borrowed eyes. If a sense is missing it says so. Port 11434. Files you can delete.

**Job:** short clip + sidecar. Honest when words fail. Ear can stay off and Tiny is still complete.

```bash
python -m pip install -e ".[dev]"
# or: pipenv install --dev
make tests
make examples
tinyear ingest examples/sample.wav --out memory/ --transcript "set a timer"
```

Empty transcript → `transcript_ok: false` and belief = `I did not catch words.`

Tests use a generated 16 kHz formant tone so they run offline.
`make examples` also writes a 6-vowel + silence corpus under `examples/out/corpus/`.

Optional real speech: `python scripts/fetch_speech.py` prints how to pull
LibriSpeech dev-clean from OpenSLR. TinyEar will not caption it for you.

## Howl pipe (test dep)

TinyHowl is a **test** dependency, not a runtime one. Ear stays complete without a mouth.

Until Howl is on PyPI it is pinned by git URL (bananey branch):

```bash
# extra on its own
pip install -e ".[howl]"
# or the same pin via Pipfile
pipenv install --dev
```

```toml
# pyproject.toml
tinyhowl @ git+https://github.com/guilt/tinyhowl.git@bananey
```

After PyPI that line becomes `tinyhowl>=0.1.2`. Sibling checkout still works
without pip (offline / self-contained):

```bash
TINYHOWL_ROOT=../tinyhowl make tests
make pipe
tinyhowl say:mama - | tinyear ingest - --out memory/ --stem mama
```

The pipe test measures accuracy (valid WAV, baby-band F0, honest miss vs supplied transcript)
and wall latency of two real processes. No cloud ASR.
