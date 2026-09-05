# Getting Started with TinyEar

## Installation

```bash
git clone https://github.com/guilt/TinyEar.git
cd TinyEar && git checkout bananey
python -m pip install -e ".[dev]"
make fixtures
tinyear ingest examples/sample.wav --out examples/out --transcript "set a timer"
tinyear ingest examples/sample.wav --out examples/out --stem silent
```

Optional Howl pipe: sibling `../tinyhowl` or `TINYHOWL_ROOT`.

See [HOW_TO_VERIFY.md](../../HOW_TO_VERIFY.md).
