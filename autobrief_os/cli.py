from __future__ import annotations

import argparse
import json
import sys

from .runner import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="AutoBrief OS CLI")
    parser.add_argument("--config", required=True, help="Path to config YAML/JSON")
    parser.add_argument("--print-telegram", action="store_true", help="Print telegram summary")
    args = parser.parse_args()

    try:
        result = run_pipeline(args.config)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps({k: v for k, v in result.items() if k != "telegram_summary"}, indent=2))
    if args.print_telegram:
        print("\n--- Telegram Summary ---")
        print(result["telegram_summary"])


if __name__ == "__main__":
    main()
