#!/usr/bin/env python3
"""Validate the Agent Skill catalog without third-party packages."""

import argparse
import json
from pathlib import Path
import re
import sys


ALLOWED_AGENTS = {
    "codex",
    "claude-code",
    "cursor",
    "openclaw",
    "workbuddy",
    "deepseek-harness",
}


def validate(path: Path) -> dict:
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if catalog.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    if not catalog.get("catalog_id"):
        raise ValueError("catalog_id is required")
    skills = catalog.get("skills")
    if not isinstance(skills, list):
        raise ValueError("skills must be a list")
    seen = set()
    for entry in skills:
        skill_id = entry.get("id")
        if not isinstance(skill_id, str) or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_id
        ):
            raise ValueError(f"invalid skill id: {skill_id!r}")
        if skill_id in seen:
            raise ValueError(f"duplicate skill id: {skill_id}")
        seen.add(skill_id)
        if entry.get("visibility") not in {"public", "private"}:
            raise ValueError(f"invalid visibility for {skill_id}")
        repository = entry.get("repository")
        if repository is not None and not re.fullmatch(r"[^/]+/[^/]+", repository):
            raise ValueError(f"invalid repository for {skill_id}")
        agents = entry.get("supported_agents")
        if not isinstance(agents, list) or not agents:
            raise ValueError(f"supported_agents required for {skill_id}")
        unknown = set(agents) - ALLOWED_AGENTS
        if unknown:
            raise ValueError(f"unsupported agents for {skill_id}: {sorted(unknown)}")
        if entry.get("status") == "active" and repository is None:
            raise ValueError(f"active skill has no repository: {skill_id}")
    return {"status": "valid", "skill_count": len(skills)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog")
    args = parser.parse_args()
    try:
        print(json.dumps(validate(Path(args.catalog)), indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())

