from autobrief_os.config import load_config


def test_load_yaml_config(tmp_path):
    cfg = tmp_path / "c.yaml"
    cfg.write_text("sqlite_path: ./a.db\ncollectors:\n  trading:\n    enabled: true\n", encoding="utf-8")
    out = load_config(cfg)
    assert out["sqlite_path"] == "./a.db"
    assert out["collectors"]["trading"]["enabled"] is True
