# TinyEar datasets

Tests and examples are **offline**.

| set | what | words? |
|-----|------|--------|
| generated tone | 16 kHz formant-ish wav from `tinyear.fixtures` | no — `transcript_ok: false` unless you pass `--transcript` |
| generated corpus | `examples/make_corpus.py` writes 6 vowels + silence | empty on purpose |
| optional LibriSpeech | `python scripts/fetch_speech.py` prints the OpenSLR URL | you type the words |

TinyEar never invents a transcript. Empty string → belief is
`I did not catch words.`
