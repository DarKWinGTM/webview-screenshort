from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def policy_preset_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "support" / "policies"


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def _fallback_family_and_name(stem: str) -> Tuple[str, str]:
    if "-" in stem:
        family, name = stem.split("-", 1)
        return family, name
    return "custom", stem


def load_policy_preset_record(path: Path) -> Dict[str, Any]:
    payload = _load_json(path)
    family = str(payload.get("family") or "").strip()
    name = str(payload.get("name") or "").strip()
    if not family or not name:
        fallback_family, fallback_name = _fallback_family_and_name(path.stem)
        family = family or fallback_family
        name = name or fallback_name

    selector = str(payload.get("selector") or f"{family}/{name}")
    aliases = [str(alias) for alias in payload.get("aliases") or []]
    aliases = list(dict.fromkeys([path.stem, selector, *aliases]))

    return {
        "name": name,
        "family": family,
        "selector": selector,
        "path": str(path),
        "aliases": aliases,
        "policy": payload,
    }


def list_policy_preset_records() -> List[Dict[str, Any]]:
    base_dir = policy_preset_dir()
    if not base_dir.exists():
        raise FileNotFoundError(f"Policy preset directory not found: {base_dir}")

    records = [load_policy_preset_record(path) for path in sorted(base_dir.glob("*.json"))]
    if not records:
        raise FileNotFoundError(f"No built-in policy presets found in: {base_dir}")
    return records


def resolve_policy_preset_record(selector: str) -> Dict[str, Any]:
    normalized = selector.strip()
    for record in list_policy_preset_records():
        if normalized == record["selector"] or normalized in record["aliases"]:
            return record
    raise FileNotFoundError(f"Unknown policy preset: {selector}")


def list_policy_presets_payload() -> Dict[str, Any]:
    records = list_policy_preset_records()
    return {
        "policy_preset_count": len(records),
        "directory": str(policy_preset_dir()),
        "presets": records,
    }
