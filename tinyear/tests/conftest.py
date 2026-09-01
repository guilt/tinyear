"""Make TinyHowl importable for the process-pipe tests.

Howl is a TinyEar *test* dep, not runtime. Resolution order:

1. TINYHOWL_ROOT
2. sibling checkout (`../tinyhowl`) or vendored tree
3. an already-installed package (`pip install -e ".[howl]"` / git+https / later PyPI)
"""
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
        vendor = parent / "vendor" / "tinyhowl"
        if (vendor / "tinyhowl" / "__init__.py").is_file():
            return vendor
        sib = parent.parent / "tinyhowl"
        if (sib / "tinyhowl" / "__init__.py").is_file():
            return sib
    try:
        import tinyhowl

        pkg = Path(tinyhowl.__file__).resolve().parent
        root = pkg.parent
        if (root / "tinyhowl" / "__init__.py").is_file():
            return root
    except ImportError:
        return None
    return None


HOWL_ROOT = _howl_root()
if HOWL_ROOT is not None and str(HOWL_ROOT) not in sys.path:
    sys.path.insert(0, str(HOWL_ROOT))
