from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import Collector
from ..exceptions import CollectorError


class TradingStateCollector(Collector):
    name = "trading_state"

    def __init__(self, source_log_path: str, max_lines: int = 200) -> None:
        self.source_log_path = source_log_path
        self.max_lines = max_lines

    def collect(self) -> dict[str, Any]:
        p = Path(self.source_log_path)
        if not p.exists():
            raise CollectorError(f"Trading log not found: {p}")

        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()[-self.max_lines :]
        open_positions = sum(1 for l in lines if "POSITION_OPEN" in l)
        closed_positions = sum(1 for l in lines if "POSITION_CLOSED" in l)
        errors = [l for l in lines if "ERROR" in l or "WARN" in l]

        return {
            "source": str(p),
            "lines_scanned": len(lines),
            "open_positions_events": open_positions,
            "closed_positions_events": closed_positions,
            "warning_or_error_count": len(errors),
            "latest_events": lines[-10:],
        }
