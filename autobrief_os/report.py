from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def build_report(runs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collector_runs": runs,
    }


def write_json(report: dict[str, Any], output_path: str) -> None:
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def to_markdown(report: dict[str, Any]) -> str:
    lines = ["# AutoBrief OS Report", "", f"Generated: {report['generated_at']}", ""]
    for run in report.get("collector_runs", []):
        lines.append(f"## {run['collector_name']} ({run['status']})")
        lines.append(f"- Created At: {run['created_at']}")
        payload = run.get("payload", {})
        for k, v in payload.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    return "\n".join(lines)


def write_markdown(markdown: str, output_path: str) -> None:
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(markdown, encoding="utf-8")


def telegram_summary(report: dict[str, Any], max_chars: int = 3500) -> str:
    lines = ["📊 *AutoBrief OS Summary*", ""]
    for run in report.get("collector_runs", [])[:10]:
        lines.append(f"• *{run['collector_name']}* — `{run['status']}`")
        payload = run.get("payload", {})
        if run["collector_name"] == "system_health":
            lines.append(
                f"  CPU: {payload.get('cpu_count')} | Disk Free: {payload.get('disk_free_gb')} GB"
            )
        if run["collector_name"] == "trading_state":
            lines.append(
                "  OpenEvt: {0} | ClosedEvt: {1} | Warn/Err: {2}".format(
                    payload.get("open_positions_events"),
                    payload.get("closed_positions_events"),
                    payload.get("warning_or_error_count"),
                )
            )
    text = "\n".join(lines)
    return text[:max_chars]
