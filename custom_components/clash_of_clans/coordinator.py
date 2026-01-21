from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import ClashOfClansApi
from .const import DOMAIN, CONF_API_TOKEN, CONF_PLAYER_TAG

_LOGGER = logging.getLogger(__name__)


class ClashOfClansCoordinator(DataUpdateCoordinator):
    """Coordinator for Clash of Clans data."""

    def __init__(self, hass, entry):
        self.api = ClashOfClansApi(entry.data[CONF_API_TOKEN])
        self.player_tag = entry.data[CONF_PLAYER_TAG]

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Fetch data from Clash of Clans API."""
        try:
            player = await self.api.get_player(self.player_tag)
            return {
                "player": player
            }
        except Exception as err:
            raise UpdateFailed(f"Error fetching Clash of Clans data: {err}") from err