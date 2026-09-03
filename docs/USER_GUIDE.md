# TinyEar User Guide

## Where to start

| I want to... | Section |
|---|---|
| Ingest a WAV | [Ingest](#ingest) |
| Keep misses honest | [Honest miss](#honest-miss) |
| Read the sidecar | [Sidecar](#sidecar) |
| Classify atoms | [Classifier](#classifier) |
| Pipe from Howl | [Howl pipe](#howl-pipe) |

---

## Contract

Ear writes files you can delete. It does not run a cloud ASR.

- Empty transcript → `transcript_ok: false` and Belief `I did not catch words.`
- A supplied transcript is stored as-is. Ear does not check that it matches the audio.
- `class_*` fields are measurements, not words.

---

## Ingest

```bash
tinyear ingest clip.wav --out memory/ --transcript "set a timer"
tinyear ingest - --out memory/ --stem coo < clip.wav
```

```python
from tinyear import ingest_wav
ingest_wav("clip.wav", "memory", transcript="set a timer")
```

---

## Honest miss

`MISS = "I did not catch words."` Silence, coos, and inventory atoms have
no words. Never invent "hello" because the clip was voiced.

---

## Classifier

`classify_pcm` is cheap: energy gate → silence; spectral tilt → fricative
vs voiced; Goertzel F1/F2 bins → nearest of `i e a o u schwa`. Inventory
tagger, not a speech recognizer.

---

## Howl pipe

```bash
tinyhowl coo - | tinyear ingest - --out /tmp/ear --stem coo
make pipe
```
