# TinyEar — Honest Ears for Tiny

[![GitHub](https://img.shields.io/badge/GitHub-guilt/TinyEar-181717?logo=github)](https://github.com/guilt/TinyEar)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![docs](https://img.shields.io/badge/docs-USER_GUIDE-0A66C2)](docs/USER_GUIDE.md)

Tiny is a markdown cache that can grow ears, a mouth, and borrowed eyes. If a sense is missing it says so. Port 11434. Files you can delete.

Ear writes a short clip plus a sidecar. When words fail it says
`I did not catch words.` It never invents a transcript.

```bash
python -m pip install -e ".[dev]"
make tests
tinyear ingest examples/sample.wav --out memory/ --transcript "set a timer"
tinyhowl coo - | tinyear ingest - --out memory/ --stem coo
```

## The core idea

Words are a human field. Acoustics (energy, F0, F1/F2, manner) are
measurements. `classify` labels manner + nearest vowel atom with Goertzel
and spectral tilt. That is not ASR.

## Capabilities

| Feature | What it does |
|---|---|
| `ingest` | WAV or stdin → `stem.ear.wav` + `stem.ear.md` |
| Honest miss | empty transcript → `I did not catch words.` |
| Acoustics | `pitch_mean_hz`, `energy`, F1/F2, ZCR |
| Classifier | manner + nearest vowel + place |
| Howl pipe | process-to-process WAV on stdin |
| C twin | [TinyEar-C](https://github.com/guilt/TinyEar-C) targets ESP32-S3 |

## Quick start

```bash
git clone https://github.com/guilt/TinyEar.git
cd TinyEar && git checkout bananey
python -m pip install -e ".[dev]"
make tests && make examples
```

Until PyPI: `pip install "tinyear @ git+https://github.com/guilt/tinyear.git@bananey"`

Howl is a *test* extra, not runtime (`tinyhowl @ git+https://github.com/guilt/tinyhowl.git@bananey`).

## Documentation

| I want to... | Page |
|---|---|
| Get running in 5 minutes | [Getting Started](docs/source/getting_started.md) |
| Understand the ear | [User Guide](docs/USER_GUIDE.md) |
| Ingest a clip | [How-To: Ingest](docs/source/how_to/02_ingest.md) |
| Keep misses honest | [How-To: Honest miss](docs/source/how_to/03_honest_miss.md) |
| Look up a symbol | [API Reference](docs/source/api/README.md) |

## Development

```
make tests            pytest with coverage (gate ≥ 80%)
make fixtures         examples/sample.wav
make corpus           offline vowel + silence set
make pipe             Howl stdout → Ear stdin
make examples         ingest sample + corpus
make docs             regenerate API docs + Sphinx HTML
```

## Family

- [TinyHowl](https://github.com/guilt/TinyHowl) — mouth that feeds this ear
- [TinyToT](https://github.com/guilt/TinyToT) — inference server
- [TinyEye](https://github.com/guilt/TinyEye) — JPEG + belief sidecar
- [NanoToT](https://github.com/guilt/NanoToT) — clone / child packer
- [TinyEar-C](https://github.com/guilt/TinyEar-C) — C / ESP32-S3 twin

## Links

- **GitHub**: [github.com/guilt/TinyEar](https://github.com/guilt/TinyEar)
- **Docs**: [USER_GUIDE](docs/USER_GUIDE.md) · [Getting started](docs/source/getting_started.md) · [API](docs/source/api/README.md)
- **C twin**: [TinyEar-C](https://github.com/guilt/TinyEar-C)

## License

MIT — see [LICENSE.md](LICENSE.md).
