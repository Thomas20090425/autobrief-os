from pathlib import Path

from autobrief_os.runner import run_pipeline


def test_pipeline_generates_outputs(tmp_path):
    log = tmp_path / "trading.log"
    log.write_text("POSITION_OPEN X\nPOSITION_CLOSED X\n", encoding="utf-8")
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        f"""
sqlite_path: {tmp_path}/autobrief.db
output_dir: {tmp_path}/out
collectors:
  trading:
    enabled: true
    source_log_path: {log}
    max_lines: 100
  system_health:
    enabled: true
report:
  markdown_filename: report.md
  json_filename: report.json
telegram:
  max_chars: 1000
retry:
  attempts: 2
  base_delay_seconds: 0.0
""",
        encoding="utf-8",
    )

    res = run_pipeline(str(cfg))
    assert Path(res["output_markdown"]).exists()
    assert Path(res["output_json"]).exists()
    assert "AutoBrief OS Summary" in res["telegram_summary"]
