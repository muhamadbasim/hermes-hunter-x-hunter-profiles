#!/usr/bin/env python3
"""Exercise every generated distribution through the installed Hermes CLI."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )


def main() -> int:
    hermes = os.environ.get("HERMES_BIN", "hermes")
    if shutil.which(hermes) is None:
        raise SystemExit(f"Hermes executable not found: {hermes}")
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(dir="/tmp", prefix="hxh_profiles_e2e_") as temp:
        home = Path(temp) / "hermes"
        home.mkdir()
        env = dict(os.environ)
        env.update({"HERMES_HOME": str(home), "BWS_ACCESS_TOKEN": ""})
        for persona in catalog:
            slug = persona["slug"]
            print(f"  Testing install: {slug}", flush=True)
            proc = run(
                [
                    hermes,
                    "profile",
                    "install",
                    str(ROOT / "profiles" / slug),
                    "--name",
                    slug,
                    "-y",
                ],
                env=env,
            )
            if proc.returncode:
                raise SystemExit(f"Install failed for {slug}:\n{proc.stdout}\n{proc.stderr}")
            installed = home / "profiles" / slug
            soul = (installed / "SOUL.md").read_text(encoding="utf-8")
            config = yaml.safe_load((installed / "config.yaml").read_text(encoding="utf-8"))
            skin = yaml.safe_load((installed / "skins" / f"{slug}.yaml").read_text(encoding="utf-8"))
            assert persona["name"] in soul
            assert config == {"model": "", "display": {"skin": slug}}
            assert skin["branding"]["agent_name"] == persona["name"]

        # Test state-preserving update on sample
        sample = home / "profiles" / "ging-freecss"
        (sample / "memories" / "MEMORY.md").write_text("LOCAL MEMORY\n", encoding="utf-8")
        (sample / "config.yaml").write_text("model: local-model\ndisplay:\n  skin: local-skin\n", encoding="utf-8")
        (sample / "SOUL.md").write_text("STALE\n", encoding="utf-8")
        proc = run([hermes, "profile", "update", "ging-freecss", "-y"], env=env)
        if proc.returncode:
            raise SystemExit(f"Update failed:\n{proc.stdout}\n{proc.stderr}")
        assert "Ging Freecss" in (sample / "SOUL.md").read_text(encoding="utf-8")
        assert "local-model" in (sample / "config.yaml").read_text(encoding="utf-8")
        assert (sample / "memories" / "MEMORY.md").read_text(encoding="utf-8") == "LOCAL MEMORY\n"

    print(f"E2E validated {len(catalog)} profile installs and one preserving update")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
