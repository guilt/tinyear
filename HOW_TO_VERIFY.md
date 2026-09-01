# HOW_TO_VERIFY — TinyEar

```bash
python -m pip install -e ".[dev]"
make tests
make examples
grep transcript_ok examples/out/*.ear.md examples/out/corpus/*.ear.md
```

Expect:

- `examples/out/sample.ear.md` has `transcript_ok: true` and `set a timer`
- `examples/out/silent.ear.md` has `transcript_ok: false` and `I did not catch words.`
- corpus sidecars are honest misses (no invented words)
- `pitch_mean_hz` and `energy` present on every sidecar

## Howl → Ear process pipe

Needs a sibling `../tinyhowl` checkout (or `TINYHOWL_ROOT`).

```bash
TINYHOWL_ROOT=../tinyhowl PYTHONPATH=../tinyhowl:. python -m pytest tinyear/tests/test_howl_pipe.py -q -s
make pipe
tinyhowl coo - | tinyear ingest - --out /tmp/ear --stem coo
```

Expect:

- howl and ear exit 0
- `/tmp/ear/coo.ear.wav` is RIFF/WAVE 16 kHz
- sidecar `transcript_ok: false` and `I did not catch words.` unless `--transcript` is passed
- `pitch_mean_hz` in a baby band (~120–900)
- wall time of the two-process pipe well under 8 s on a laptop
