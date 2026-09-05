#!/usr/bin/env python3
import sys
from pathlib import Path
import urllib.request
URL = "https://www.openslr.org/resources/12/dev-clean.tar.gz"

def main() -> int:
    print("tinyear ships its own tone fixture. Network speech is optional.")
    print("LibriSpeech dev-clean:")
    print("  curl -L", URL, "-o /tmp/dev-clean.tar.gz")
    print("  ffmpeg -i foo.flac -ar 16000 -ac 1 examples/librispeech.wav")
    if "--download" in sys.argv:
        dest = Path("examples/dev-clean.tar.gz")
        dest.parent.mkdir(exist_ok=True)
        urllib.request.urlretrieve(URL, dest)
        print("wrote", dest)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
