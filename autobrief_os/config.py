from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .exceptions import ConfigError


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    """
    Minimal parser for simple key/value + nested blocks used by config.example.yaml.
    For production, replace with PyYAML/ruamel if dependency policy allows.
    """
    out: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(0, out)]

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        while stack and indent < stack[-1][0]:
            stack.pop()
        if not stack:
            raise ConfigError("Invalid indentation in config")

        current = stack[-1][1]

        if ":" not in stripped:
            raise ConfigError(f"Invalid config line: {raw_line}")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            child: dict[str, Any] = {}
            current[key] = child
            stack.append((indent + 2, child))
        else:
            val: Any
            if value.lower() in {"true", "false"}:
                val = value.lower() == "true"
            else:
                try:
                    if "." in value:
                        val = float(value)
                    else:
                        val = int(value)
                except ValueError:
                    val = value
            current[key] = val

    return out


def load_config(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise ConfigError(f"Config file not found: {p}")

    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".json":
        return json.loads(text)
    if p.suffix.lower() in {".yaml", ".yml"}:
        return _parse_simple_yaml(text)
    raise ConfigError("Config must be .json/.yaml/.yml")
