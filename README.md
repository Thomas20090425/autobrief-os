# AutoBrief OS

Production-minded daily briefing system built in Python + SQLite.

Author: **Thomas20090425**

## What it does

- Runs modular collectors:
  - Trading state/log collector
  - System health collector
- Persists collector outputs into SQLite
- Generates report artifacts:
  - Markdown report
  - JSON report
- Produces Telegram-ready summary text
- Provides CLI entrypoint for local/cron automation

## Architecture

- `autobrief_os/config.py` — config loader (`.yaml`/`.json`)
- `autobrief_os/collectors/` — modular collector interfaces + implementations
- `autobrief_os/db.py` — SQLite schema and persistence
- `autobrief_os/runner.py` — orchestrates retries, collectors, persistence, report output
- `autobrief_os/report.py` — markdown/json emitters + Telegram summary formatter
- `autobrief_os/cli.py` — CLI interface (`autobrief`)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp config.example.yaml config.yaml
```

Edit `config.yaml`, especially:

- `sqlite_path`
- `collectors.trading.source_log_path`
- `output_dir`

## Usage

```bash
autobrief --config ./config.yaml --print-telegram
```

Outputs are written to configured `output_dir`.

## Testing

```bash
pip install pytest
pytest -q
```

## Error Handling / Retries

- Collector execution uses configurable retries (`retry.attempts`, `retry.base_delay_seconds`)
- Collector failures are captured into SQLite with `status=error` and included in reports
- CLI exits non-zero on fatal pipeline/config errors

## Limitations

- YAML parsing is intentionally minimal (supports simple nested maps only)
- Trading collector currently parses plain text log events (not exchange APIs)
- System health collector is host-local and lightweight (no deep telemetry stack)

## License

MIT — see `LICENSE`.
