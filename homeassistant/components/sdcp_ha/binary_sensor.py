"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import Event, HomeAssistant
from homeassistant.components.binary_sensor import (
    BinarySensorEntity
)

from .const import DOMAIN
from .coordinator import SDCPCoordinator
from .sdcp import discover_printers


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for past config_entry in HA."""

    new_devices = []

    # printers = await discover_printers()

    # for printer in printers:
    #     new_devices.append(PrinterOnOffSensor(printer))

    ip = "192.168.4.185"

    coordinator = SDCPCoordinator(hass, ip)
    await coordinator.sio_connect()

    async def _async_sio_close(_: Event) -> None:
        await coordinator.sio_close()

    config_entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_sio_close)
    )

    new_devices.append(PrinterOnOffSensor(hass, { "id": "f25273b12b094c5a8b9513a30ca60049", "brand": "ELEGOO", "model": "Saturn 4 Ultra", "name": "Saturn IV Utra", "ip": ip, "mainboardID": "c441065fe0fa0100", "protocol": "V3.0.0", "firmware": "V1.2.8" }, coordinator))

    if new_devices:
        async_add_entities(new_devices)

class PrinterOnOffSensor(BinarySensorEntity):
    def __init__(self, hass: HomeAssistant, printer: dict, coordinator: SDCPCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__()
        self._attr_has_entity_name = True
        self._attr_device_info = DeviceInfo(
            manufacturer=printer['brand'],
            model=printer['model'],
            name=printer['name']
        )
        self._attr_unique_id = self.printer['mainboardID']
        self.printer = printer
        self._value = True

        self.coordinator = coordinator

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def name(self) -> str | None:
        return "Running State"

    @property
    def native_value(self) -> bool | None:
        """Raw value of the sensor"""
        return self._value

    @property
    def is_on(self) -> bool:
        """Return if the pump is running."""
        return self._value

    @property
    def icon(self) -> str:
        if self._value is True:
            return "mdi:pump"
        return "mdi:pump-off"