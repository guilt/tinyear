# TinyEar

Tiny is a markdown cache that can grow ears, a mouth, and borrowed eyes. If a sense is missing it says so. Port 11434. Files you can delete.

**Job:** short clip + sidecar. Honest when words fail.

The watch has a PDM mic. Ear can stay **off** and Tiny is still complete.

```bash
python -m tinyear ingest sample.wav --out memory/
ls memory/*.ear.md memory/*.ear.*
grep transcript_ok memory/*.ear.md
```

If words fail: `transcript_ok: false`, belief = acoustics + “I did not catch words.”
No cloud ASR in v0.1.
