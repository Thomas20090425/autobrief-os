from __future__ import annotations

import os
import platform
import shutil
from datetime import datetime, timezone
from typing import Any

from .base import Collector


class SystemHealthCollector(Collector):
    name = "system_health"

    def collect(self) -> dict[str, Any]:
        load_avg = None
        try:
            if hasattr(os, "getloadavg"):
                load_avg = os.getloadavg()
        except OSError:
            load_avg = None

        disk = shutil.disk_usage("/")
        return {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu_count": os.cpu_count(),
            "load_avg": load_avg,
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_used_gb": round(disk.used / (1024**3), 2),
            "disk_free_gb": round(disk.free / (1024**3), 2),
        }
