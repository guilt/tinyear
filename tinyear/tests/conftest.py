"""Make sibling TinyHowl importable. Howl is a TinyEar *test* dep, not runtime."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _howl_root() -> Path | None:
    env = os.environ.get("TINYHOWL_ROOT")
    if env:
        p = Path(env)
        return p if (p / "tinyhowl").is_dir() else None
    here = Path(__file__).resolve()
    for parent in here.parents:
        cand = parent / "tinyhowl"
        if (cand / "tinyhowl" / "__init__.py").is_file():
            return cand
        sib = parent.parent / "tinyhowl"
        if (sib / "tinyhowl" / "__init__.py").is_file():
            return sib
    return None


HOWL_ROOT = _howl_root()
if HOWL_ROOT is not None:
    sys.path.insert(0, str(HOWL_ROOT))
