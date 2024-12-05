"""SDCP integration using DataUpdateCoordinator."""

from datetime import timedelta
import logging

import socketio

import async_timeout

from homeassistant.components.light import LightEntity
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, EVENT_AVAILABILITY

logger = logging.getLogger(__name__)


class SDCPCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, ip: str):
        super().__init__(
            hass,
            logger,
            name="SDCP",
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True
        )
        self.sio = None
        self.ip = ip

    async def sio_connect(self):
        """Method to connect to nodejs-PoolController"""

        self.sio = socketio.AsyncClient(
            reconnection=True,
            reconnection_attempts=0,
            reconnection_delay=1,
            reconnection_delay_max=10,
            logger=False,
            engineio_logger=False,
        )
        logging.getLogger("socketio.client").setLevel(logging.ERROR)
        logging.getLogger("engineio.client").setLevel(logging.ERROR)

        @self.sio.event
        async def connect():
            print("I'm connected!")
            avail = {"event": EVENT_AVAILABILITY, "available": True}
            self.async_set_updated_data(avail)
            self.logger.debug(f"SocketIO connected to {self.ip}")

        @self.sio.event
        async def connect_error(data):
            avail = {"event": EVENT_AVAILABILITY, "available": False}
            self.async_set_updated_data(avail)
            self.logger.error(f"SocketIO connection error: {data}")
            print("The connection failed!")

        @self.sio.event
        async def disconnect():
            avail = {"event": EVENT_AVAILABILITY, "available": False}
            self.async_set_updated_data(avail)
            self.logger.debug(f"SocketIO disconnect to {self.api.get_base_url()}")
            print("I'm disconnected!")

        url = f"ws://{self.ip}:3030/websocket"
        try:
            await self.sio.connect(url)
        except socketio.exceptions.ConnectionError as err:
            logger.error(f'Error connecting to socket {url}', err)
        except:
            logger.error(f'Unknown error connecting to socket {url}')

    async def sio_close(self):
        """Close the socket"""
        await self.sio.disconnect()

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        # self._device = await self.my_api.get_device()
        pass

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        # try:
        #     # Note: asyncio.TimeoutError and aiohttp.ClientError are already
        #     # handled by the data update coordinator.
        #     async with async_timeout.timeout(10):
        #         # Grab active context variables to limit data required to be fetched from API
        #         # Note: using context is not required if there is no need or ability to limit
        #         # data retrieved from API.
        #         listening_idx = set(self.async_contexts())
        #         return await self.my_api.fetch_data(listening_idx)
        # except ApiAuthError as err:
        #     # Raising ConfigEntryAuthFailed will cancel future updates
        #     # and start a config flow with SOURCE_REAUTH (async_step_reauth)
        #     raise ConfigEntryAuthFailed from err
        # except ApiError as err:
        #     raise UpdateFailed(f"Error communicating with API: {err}")
        pass


class MyEntity(CoordinatorEntity, LightEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.coordinator.data[self.idx]["state"]
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Turn the light on.

        Example method how to request data updates.
        """
        # Do the turning on.
        # ...

        # Update the data
        await self.coordinator.async_request_refresh()

