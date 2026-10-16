#!/usr/bin/env python3
"""Publishes every GitHub release of the mods listed in artifacts.json that is not in this repository yet."""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORG = "GTInfinityAscension"


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


for entry in json.loads((ROOT / "artifacts.json").read_text()):
    base = ROOT / entry["group"].replace(".", "/") / entry["artifact"]
    releases = json.loads(gh("release", "list", "-R", f"{ORG}/{entry['repo']}", "-L", "5",
                             "--exclude-drafts", "--json", "tagName"))
    for tag in reversed([r["tagName"] for r in releases]):
        version = tag.removeprefix("v")
        if (base / version).exists():
            continue
        asset = entry["asset"].format(version=version)
        with tempfile.TemporaryDirectory() as tmp:
            try:
                gh("release", "download", tag, "-R", f"{ORG}/{entry['repo']}", "-p", asset, "-D", tmp)
            except subprocess.CalledProcessError:
                print(f"skip {entry['repo']} {tag}: no asset {asset}")
                continue
            subprocess.run(["python3", str(ROOT / "tools/deploy.py"), entry["group"], entry["artifact"], version,
                            str(Path(tmp) / asset)], check=True)
