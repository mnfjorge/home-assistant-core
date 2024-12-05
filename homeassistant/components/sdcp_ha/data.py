from __future__ import annotations

from dataclasses import dataclass
from homeassistant.loader import Integration

from .coordinator import SDCPCoordinator


@dataclass
class SDCPData:
    coordinator: SDCPCoordinator
    integration: Integration