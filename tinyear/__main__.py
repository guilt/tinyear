from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ingest import ingest_bytes, ingest_wav


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tinyear")
    sub = p.add_subparsers(dest="cmd", required=True)
    ing = sub.add_parser("ingest")
    ing.add_argument("wav")
    ing.add_argument("--out", type=Path, default=Path("memory"))
    ing.add_argument("--transcript", default="")
    ing.add_argument("--stem", default=None)
    ing.add_argument("--source", default=None)
    args = p.parse_args(argv)
    if args.cmd == "ingest":
        if args.wav in ("-", "/dev/stdin"):
            blob = sys.stdin.buffer.read()
            stem = args.stem or "stdin"
            wav, md = ingest_bytes(
                blob,
                args.out,
                stem,
                transcript=args.transcript,
                source=args.source or "pipe",
            )
        else:
            wav, md = ingest_wav(
                Path(args.wav),
                args.out,
                transcript=args.transcript,
                stem=args.stem,
                source=args.source or "desktop",
            )
        print(wav)
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
