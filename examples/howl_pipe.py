#!/usr/bin/env python3
"""Howl mouth → Ear sidecar over a real OS pipe.

  PYTHONPATH=../tinyhowl:. python examples/howl_pipe.py
  tinyhowl say:mama - | tinyear ingest - --out examples/out --stem mama
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EAR_ROOT = HERE.parent
HOWL_ROOT = Path(os.environ.get("TINYHOWL_ROOT", EAR_ROOT.parent / "tinyhowl"))
OUT = HERE / "out"


def main() -> int:
    OUT.mkdir(exist_ok=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [str(HOWL_ROOT), str(EAR_ROOT), env.get("PYTHONPATH", "")]
    )
    howl = subprocess.Popen(
        [sys.executable, "-m", "tinyhowl.demo", "say:mama", "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        cwd=str(HOWL_ROOT),
    )
    ear = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "tinyear",
            "ingest",
            "-",
            "--out",
            str(OUT),
            "--stem",
            "howl-mama",
            "--source",
            "howl-pipe",
        ],
        stdin=howl.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        cwd=str(EAR_ROOT),
    )
    if howl.stdout is not None:
        howl.stdout.close()
    out, err = ear.communicate(timeout=20)
    howl.wait(timeout=20)
    print(out.decode("utf-8", "replace"), end="")
    if ear.returncode != 0:
        print(err.decode("utf-8", "replace"), file=sys.stderr)
        return ear.returncode
    md = OUT / "howl-mama.ear.md"
    print(md.read_text(encoding="utf-8") if md.exists() else "missing sidecar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
