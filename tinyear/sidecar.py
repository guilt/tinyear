"""Parse / write *.ear.md. Indexes yaml + ## Belief only."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    text = text.replace("\r\n", "\n")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, Any] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        val = v.strip()
        if val in ("true", "false"):
            meta[k.strip()] = val == "true"
        else:
            meta[k.strip()] = val
    return meta, body


def extract_belief(body: str) -> str:
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower() == "## belief":
            start = i + 1
            break
    if start is None:
        return ""
    chunk = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        chunk.append(line)
    return "\n".join(chunk).strip()


@dataclass
class EarSidecar:
    path: Path
    meta: dict[str, Any] = field(default_factory=dict)
    belief: str = ""
    wav_path: str | None = None

    @property
    def transcript_ok(self) -> bool:
        return bool(self.meta.get("transcript_ok"))


def parse_ear(path: Path) -> EarSidecar:
    text = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    stem = path.name[: -len(".ear.md")] if path.name.endswith(".ear.md") else path.stem
    wav = path.with_name(f"{stem}.ear.wav")
    return EarSidecar(
        path=path,
        meta=meta,
        belief=extract_belief(body),
        wav_path=str(wav) if wav.exists() else None,
    )
