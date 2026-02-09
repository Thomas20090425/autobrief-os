from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS collector_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  collector_name TEXT NOT NULL,
  status TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
"""


def get_conn(sqlite_path: str) -> sqlite3.Connection:
    Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(sqlite_path)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def insert_collector_run(conn: sqlite3.Connection, collector_name: str, status: str, payload: dict[str, Any]) -> None:
    conn.execute(
        "INSERT INTO collector_runs(collector_name, status, payload_json, created_at) VALUES(?,?,?,?)",
        (
            collector_name,
            status,
            json.dumps(payload, ensure_ascii=False),
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()


def fetch_latest_runs(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT collector_name, status, payload_json, created_at
        FROM collector_runs
        ORDER BY id DESC
        """
    ).fetchall()
    out = []
    for name, status, payload_json, created_at in rows:
        out.append(
            {
                "collector_name": name,
                "status": status,
                "payload": json.loads(payload_json),
                "created_at": created_at,
            }
        )
    return out
