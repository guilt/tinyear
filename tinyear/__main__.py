from __future__ import annotations
import argparse
from pathlib import Path
from .ingest import ingest_wav

def main() -> int:
    p = argparse.ArgumentParser(prog="tinyear")
    sub = p.add_subparsers(dest="cmd", required=True)
    ing = sub.add_parser("ingest")
    ing.add_argument("wav", type=Path)
    ing.add_argument("--out", type=Path, default=Path("memory"))
    ing.add_argument("--transcript", default="")
    ing.add_argument("--stem", default=None)
    args = p.parse_args()
    if args.cmd == "ingest":
        wav, md = ingest_wav(args.wav, args.out, transcript=args.transcript, stem=args.stem)
        print(wav); print(md)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
