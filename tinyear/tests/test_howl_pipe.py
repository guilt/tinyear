"""Real process→process pipe: TinyHowl stdout WAV → TinyEar stdin ingest.

Accuracy is cache-consistency, not ASR. Ear does not invent words.
Latency is wall time around two child processes + a short utterance.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tinyear.acoustics import energy, read_pcm16, voiced, zero_cross_hz
from tinyear.ingest import MISS
from tinyear.sidecar import parse_ear
from tinyear.tests.conftest import HOWL_ROOT

pytest.importorskip("tinyhowl")

EAR_ROOT = Path(__file__).resolve().parents[2]
HOWL_BUDGET_S = 8.0
INGEST_BUDGET_S = 1.0
BABY_F0_LO = 120.0
BABY_F0_HI = 900.0


def _env() -> dict:
    env = os.environ.copy()
    parts = [str(EAR_ROOT)]
    if HOWL_ROOT is not None:
        parts.insert(0, str(HOWL_ROOT))
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(parts + ([existing] if existing else []))
    env["PYTHONUNBUFFERED"] = "1"
    return env


def _pipe(kind: str, out_dir: Path, stem: str, transcript: str = "") -> dict:
    """tinyhowl <kind> - | tinyear ingest - --stem <stem>"""
    howl_cmd = [sys.executable, "-m", "tinyhowl.demo", kind, "-"]
    ear_cmd = [
        sys.executable,
        "-m",
        "tinyear",
        "ingest",
        "-",
        "--out",
        str(out_dir),
        "--stem",
        stem,
        "--source",
        "howl-pipe",
    ]
    if transcript:
        ear_cmd.extend(["--transcript", transcript])

    t0 = time.perf_counter()
    howl = subprocess.Popen(
        howl_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env(),
        cwd=str(HOWL_ROOT or EAR_ROOT),
    )
    ear = subprocess.Popen(
        ear_cmd,
        stdin=howl.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env(),
        cwd=str(EAR_ROOT),
    )
    assert howl.stdout is not None
    howl.stdout.close()
    ear_out, ear_err = ear.communicate(timeout=20)
    howl_err = howl.stderr.read() if howl.stderr else b""
    howl.wait(timeout=20)
    wall_s = time.perf_counter() - t0
    return {
        "howl_rc": howl.returncode,
        "ear_rc": ear.returncode,
        "howl_err": howl_err.decode("utf-8", "replace"),
        "ear_out": ear_out.decode("utf-8", "replace"),
        "ear_err": ear_err.decode("utf-8", "replace"),
        "wall_s": wall_s,
        "wav": out_dir / f"{stem}.ear.wav",
        "md": out_dir / f"{stem}.ear.md",
    }


def test_process_pipe_coo_honest_and_voiced(tmp_path: Path):
    result = _pipe("coo", tmp_path, "coo")
    assert result["howl_rc"] == 0, result["howl_err"]
    assert result["ear_rc"] == 0, result["ear_err"] + result["ear_out"]
    assert result["wav"].is_file() and result["wav"].stat().st_size > 44
    blob = result["wav"].read_bytes()
    assert blob[:4] == b"RIFF" and blob[8:12] == b"WAVE"

    sc = parse_ear(result["md"])
    assert sc.transcript_ok is False
    assert sc.belief == MISS
    assert sc.meta.get("source") == "howl-pipe"
    assert sc.meta.get("codec") == "wav"

    rate, samples = read_pcm16(result["wav"])
    assert rate == 16000
    assert voiced(samples, rate)
    f0 = zero_cross_hz(samples, rate)
    assert BABY_F0_LO <= f0 <= BABY_F0_HI
    assert energy(samples) >= 0.02
    assert int(sc.meta.get("duration_ms", "0")) >= 200
    assert result["wall_s"] < HOWL_BUDGET_S


def test_process_pipe_mama_transcript_accuracy(tmp_path: Path):
    result = _pipe("say:mama", tmp_path, "mama", transcript="mama")
    assert result["howl_rc"] == 0, result["howl_err"]
    assert result["ear_rc"] == 0, result["ear_err"]
    sc = parse_ear(result["md"])
    assert sc.transcript_ok is True
    assert sc.belief == "mama"
    rate, samples = read_pcm16(result["wav"])
    assert voiced(samples, rate)
    assert int(sc.meta.get("duration_ms", "0")) >= 250
    assert result["wall_s"] < HOWL_BUDGET_S


def test_process_pipe_does_not_invent_words(tmp_path: Path):
    result = _pipe("say:hi", tmp_path, "hi")
    assert result["ear_rc"] == 0, result["ear_err"]
    text = result["md"].read_text(encoding="utf-8")
    assert "transcript_ok: false" in text
    assert MISS in text
    assert "hello" not in text.lower()


def test_pipe_latency_and_accuracy_report(tmp_path: Path):
    """One table: accuracy flags + wall latency for three howls."""
    rows = []
    for kind, stem, transcript in (
        ("coo", "coo", ""),
        ("say:mama", "mama", "mama"),
        ("say:hi", "hi", ""),
    ):
        r = _pipe(kind, tmp_path / stem, stem, transcript=transcript)
        assert r["howl_rc"] == 0 and r["ear_rc"] == 0, r
        rate, samples = read_pcm16(r["wav"])
        sc = parse_ear(r["md"])
        expect_ok = bool(transcript)
        rows.append(
            {
                "kind": kind,
                "wall_ms": r["wall_s"] * 1000,
                "dur_ms": int(sc.meta.get("duration_ms", "0")),
                "f0": zero_cross_hz(samples, rate),
                "energy": energy(samples),
                "voiced": voiced(samples, rate),
                "transcript_ok": sc.transcript_ok,
                "belief": sc.belief,
                "expect_ok": expect_ok,
            }
        )

    accurate = 0
    for row in rows:
        ok = (
            row["voiced"]
            and BABY_F0_LO <= row["f0"] <= BABY_F0_HI
            and row["energy"] >= 0.02
            and row["transcript_ok"] is row["expect_ok"]
            and (row["belief"] == row["kind"].split(":")[-1] if row["expect_ok"] else row["belief"] == MISS)
            and row["wall_ms"] / 1000.0 < HOWL_BUDGET_S
        )
        row["pass"] = ok
        accurate += int(ok)

    report = tmp_path / "pipe_report.md"
    lines = [
        "# Howl → Ear pipe report",
        "",
        "| kind | wall_ms | dur_ms | f0_hz | energy | voiced | transcript_ok | pass |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['kind']} | {row['wall_ms']:.1f} | {row['dur_ms']} | "
            f"{row['f0']:.1f} | {row['energy']:.3f} | {row['voiced']} | "
            f"{row['transcript_ok']} | {row['pass']} |"
        )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report.read_text(encoding="utf-8"))
    assert accurate == len(rows)
    mean_wall = sum(r["wall_ms"] for r in rows) / len(rows)
    assert mean_wall / 1000.0 < HOWL_BUDGET_S


def test_ingest_bytes_latency_without_spawn(tmp_path: Path):
    from tinyhowl.baby import coo_samples
    from tinyhowl.synth import wav_bytes
    from tinyear.ingest import ingest_bytes

    blob = wav_bytes(coo_samples())
    t0 = time.perf_counter()
    dest, md = ingest_bytes(blob, tmp_path, "coo", source="bench")
    elapsed = time.perf_counter() - t0
    assert dest.exists() and md.exists()
    assert elapsed < INGEST_BUDGET_S
    print(f"ingest_bytes wall={elapsed * 1000:.2f}ms bytes={len(blob)}")
