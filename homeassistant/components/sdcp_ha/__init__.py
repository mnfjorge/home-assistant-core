"""The SDCP Resin Printer integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import Event, HomeAssistant

from .const import DOMAIN
# from .coordinator import SDCPCoordinator
# from .data import SDCPData
# from .sdcp import discover_printers

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SDCP Resin Printer from a config entry."""

    # coordinator = SDCPCoordinator()
    # await coordinator.sio_connect()

    # hass.data[DOMAIN][entry.entry_id] = SDCPData(
    #     integration=async_get_loaded_integration(hass, entry.domain),
    #     coordinator=coordinator,
    # )

    # await coordinator.async_config_entry_first_refresh()

    # printers = await discover_printers()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # async def _async_sio_close(_: Event) -> None:
    #     await coordinator.sio_close()

    # entry.async_on_unload(
    #     hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_sio_close)
    # )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

