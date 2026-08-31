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
