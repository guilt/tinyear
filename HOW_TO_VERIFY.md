# HOW_TO_VERIFY — TinyEar

```bash
python -m pip install -e ".[dev]"
make tests
make examples
grep transcript_ok examples/out/*.ear.md
```
