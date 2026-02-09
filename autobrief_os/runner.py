from __future__ import annotations

from pathlib import Path
from typing import Any

from . import __version__
from .collectors.system_health import SystemHealthCollector
from .collectors.trading import TradingStateCollector
from .config import load_config
from .db import fetch_latest_runs, get_conn, insert_collector_run
from .report import build_report, telegram_summary, to_markdown, write_json, write_markdown
from .retry import with_retry


def run_pipeline(config_path: str) -> dict[str, Any]:
    cfg = load_config(config_path)
    sqlite_path = cfg.get("sqlite_path", "./autobrief.db")
    output_dir = Path(cfg.get("output_dir", "./output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    conn = get_conn(sqlite_path)

    attempts = int(cfg.get("retry", {}).get("attempts", 3))
    delay = float(cfg.get("retry", {}).get("base_delay_seconds", 0.2))

    collectors = []
    if cfg.get("collectors", {}).get("trading", {}).get("enabled", False):
        tcfg = cfg["collectors"]["trading"]
        collectors.append(TradingStateCollector(tcfg.get("source_log_path", "./trading.log"), int(tcfg.get("max_lines", 200))))
    if cfg.get("collectors", {}).get("system_health", {}).get("enabled", False):
        collectors.append(SystemHealthCollector())

    for collector in collectors:
        try:
            payload = with_retry(collector.collect, attempts=attempts, base_delay_seconds=delay)
            insert_collector_run(conn, collector.name, "ok", payload)
        except Exception as exc:
            insert_collector_run(conn, collector.name, "error", {"error": str(exc)})

    runs = fetch_latest_runs(conn)
    report = build_report(runs)

    md_name = cfg.get("report", {}).get("markdown_filename", "report.md")
    json_name = cfg.get("report", {}).get("json_filename", "report.json")

    write_markdown(to_markdown(report), str(output_dir / md_name))
    write_json(report, str(output_dir / json_name))

    return {
        "version": __version__,
        "output_markdown": str(output_dir / md_name),
        "output_json": str(output_dir / json_name),
        "telegram_summary": telegram_summary(report, int(cfg.get("telegram", {}).get("max_chars", 3500))),
        "runs_count": len(runs),
    }
