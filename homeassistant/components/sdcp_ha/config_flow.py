"""Config flow for SDCP Resin Printer."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN
from .sdcp import discover_printers


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    # printers = await discover_printers()
    # return len(printers) > 0
    return True


config_entry_flow.register_discovery_flow(DOMAIN, "SDCP Resin Printer", _async_has_devices)
