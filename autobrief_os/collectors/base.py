from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Collector(ABC):
    name: str

    @abstractmethod
    def collect(self) -> dict[str, Any]:
        raise NotImplementedError
