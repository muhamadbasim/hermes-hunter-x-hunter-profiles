#!/usr/bin/env python3
"""Structural and content checks for generated Hunter x Hunter profile distributions."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
PROFILES = ROOT / "profiles"
EXPECTED_CATEGORIES = {
    "Specialist",
    "Conjurer",
    "Manipulator",
    "Transmuter",
    "Enhancer",
    "Emitter",
    "Association",
}
REQUIRED_FILES = {"distribution.yaml", "SOUL.md", "config.yaml", "README.md"}
FORBIDDEN_TRACKED_NAMES = {
    ".env", ".env.EXAMPLE", "auth.json", "state.db", "state.db-wal",
    "state.db-shm", "hermes_state.db", "response_store.db", "gateway.pid",
    "gateway_state.json", "processes.json", "auth.lock", ".update_check",
    "errors.log", ".hermes_history",
}
FORBIDDEN_TRACKED_DIRS = {
    "memories", "sessions", "logs", "plans", "workspace", "home", "local",
    "browser_screenshots", "state-snapshots", "checkpoints", "sandboxes",
    "backups", "cache", "node_modules",
}
SOUL_SECTIONS = {
    "## Identity",
    "## Non-Negotiable Boundaries",
    "## Relationship With the User",
    "## Voice",
    "## Worldview",
    "## Operating Method",
    "## Strengths to Emphasize",
    "## Under Pressure",
    "## Disagreement",
    "## Behavioral Rules",
    "## Canon Anchors",
    "## Blind Spots",
    "## Avoid",
    "## Baseline Hermes Contract",
}
SOUL_INVARIANTS = {
    "Never claim to be the fictional person",
    "Treat the user as a competent collaborator",
    "grant no real-world credentials",
    "authorization only for its clearly stated scope",
    "require a clearly identified user-controlled target or credible authorization",
    "Respect the autonomy, privacy, safety, and rights of third parties",
    "Never use coercion, covert persuasion, impersonation, fabricated evidence",
    "Never cultivate emotional or romantic exclusivity, dependency, or isolation",
    "preserve platform approval controls",
    "avoid diagnosis, prescription, guarantees, or certification",
    "rather than fabricating success or silently changing the goal",
    "Use tools when they improve correctness",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def load_catalog() -> list[dict[str, Any]]:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        fail("catalog.json must be a non-empty array")
    return data


def validate() -> None:
    catalog = load_catalog()
    slugs = [p["slug"] for p in catalog]
    if len(slugs) != len(set(slugs)):
        fail("catalog has duplicate slugs")
    cat_counts = Counter(p["category"] for p in catalog)
    if set(cat_counts) != EXPECTED_CATEGORIES:
        fail(f"category mismatch: {cat_counts}")

    profile_dirs = {p.name for p in PROFILES.iterdir() if p.is_dir()}
    if profile_dirs != set(slugs):
        fail(f"profile directory mismatch: missing={set(slugs)-profile_dirs}, extra={profile_dirs-set(slugs)}")

    for persona in catalog:
        slug = persona["slug"]
        root = PROFILES / slug
        missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
        if missing:
            fail(f"{slug}: missing {missing}")
        forbidden = [p for p in root.rglob("*") if p.is_file() and p.name in FORBIDDEN_TRACKED_NAMES]
        if forbidden:
            fail(f"{slug}: forbidden files: {forbidden}")
        forbidden_dirs = [p for p in root.rglob("*") if p.is_dir() and p.name in FORBIDDEN_TRACKED_DIRS]
        if forbidden_dirs:
            fail(f"{slug}: forbidden directories: {forbidden_dirs}")

        skin_path = root / "skins" / f"{slug}.yaml"
        if not skin_path.is_file():
            fail(f"{slug}: missing skin {skin_path.name}")
        skin_data = yaml.safe_load(skin_path.read_text(encoding="utf-8"))
        if skin_data.get("name") != slug:
            fail(f"{slug}: skin name mismatch")

        manifest = yaml.safe_load((root / "distribution.yaml").read_text(encoding="utf-8"))
        if manifest.get("name") != slug:
            fail(f"{slug}: manifest name mismatch")

        soul = (root / "SOUL.md").read_text(encoding="utf-8")
        for section in SOUL_SECTIONS:
            if section not in soul:
                fail(f"{slug}: SOUL.md missing section {section}")
        for invariant in SOUL_INVARIANTS:
            if invariant not in soul:
                fail(f"{slug}: SOUL.md missing invariant {invariant!r}")

    print(f"Validated {len(catalog)} profiles across {len(EXPECTED_CATEGORIES)} Nen categories")


def main() -> int:
    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
