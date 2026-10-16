#!/usr/bin/env python3
"""Adds one released jar to this Maven repository (layout + pom + checksums + metadata).

Usage: deploy.py GROUP ARTIFACT VERSION JAR [--dep group:artifact:version ...]
"""
import argparse
import hashlib
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def checksums(path: Path) -> None:
    data = path.read_bytes()
    for algo in ("md5", "sha1", "sha256"):
        Path(f"{path}.{algo}").write_text(hashlib.new(algo, data).hexdigest())


def pom(group: str, artifact: str, version: str, deps: list[str]) -> str:
    dep_xml = "".join(
        f"\n    <dependency><groupId>{g}</groupId><artifactId>{a}</artifactId><version>{v}</version>"
        f"<scope>runtime</scope></dependency>" for g, a, v in (d.split(":") for d in deps))
    deps_block = f"\n  <dependencies>{dep_xml}\n  </dependencies>" if deps else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>{group}</groupId>
  <artifactId>{artifact}</artifactId>
  <version>{version}</version>{deps_block}
</project>
"""


def metadata(base: Path, group: str, artifact: str) -> None:
    versions = sorted((p.name for p in base.iterdir() if p.is_dir()),
                      key=lambda v: [int(x) if x.isdigit() else x for x in v.replace("-", ".").split(".")])
    root = ET.Element("metadata")
    ET.SubElement(root, "groupId").text = group
    ET.SubElement(root, "artifactId").text = artifact
    vers = ET.SubElement(root, "versioning")
    ET.SubElement(vers, "latest").text = versions[-1]
    ET.SubElement(vers, "release").text = versions[-1]
    lst = ET.SubElement(vers, "versions")
    for v in versions:
        ET.SubElement(lst, "version").text = v
    ET.SubElement(vers, "lastUpdated").text = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    out = base / "maven-metadata.xml"
    ET.ElementTree(root).write(out, encoding="UTF-8", xml_declaration=True)
    checksums(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("group"), ap.add_argument("artifact"), ap.add_argument("version"), ap.add_argument("jar")
    ap.add_argument("--dep", action="append", default=[])
    a = ap.parse_args()
    base = ROOT / a.group.replace(".", "/") / a.artifact
    target = base / a.version
    # EN: A released version is never overwritten; publish a new version instead.
    # PT: Uma versão publicada nunca é sobrescrita; publique uma versão nova.
    # ZH: 已发布的版本永不覆盖；请发布新版本。
    if target.exists():
        raise SystemExit(f"{a.group}:{a.artifact}:{a.version} is already published")
    target.mkdir(parents=True)
    stem = f"{a.artifact}-{a.version}"
    shutil.copyfile(a.jar, target / f"{stem}.jar")
    (target / f"{stem}.pom").write_text(pom(a.group, a.artifact, a.version, a.dep))
    checksums(target / f"{stem}.jar")
    checksums(target / f"{stem}.pom")
    metadata(base, a.group, a.artifact)
    print(f"published {a.group}:{a.artifact}:{a.version}")


if __name__ == "__main__":
    main()
