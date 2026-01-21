from datetime import timedelta
import logging

import aiohttp

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import ClashOfClansApi
from .const import DOMAIN, CONF_API_TOKEN, CONF_PLAYER_TAG, CONF_PLAYER_TAGS

_LOGGER = logging.getLogger(__name__)


class ClashOfClansCoordinator(DataUpdateCoordinator):
    """Coordinator for Clash of Clans data."""


    def __init__(self, hass, entry):
        self.api = ClashOfClansApi(entry.data[CONF_API_TOKEN])
        player_tags = entry.data.get(CONF_PLAYER_TAGS)
        if player_tags is None:
            player_tag = entry.data.get(CONF_PLAYER_TAG)
            player_tags = [player_tag] if player_tag else []

        self.player_tags = [t for t in player_tags if t]

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )


    async def _async_update_data(self):
        """Fetch data from Clash of Clans API."""
        try:
            players: dict[str, dict] = {}
            wars: dict[str, dict | None] = {}

            for player_tag in self.player_tags:
                player = await self.api.get_player(player_tag)
                players[player_tag] = player

                war = None
                clan_tag = player.get("clan", {}).get("tag")
                if clan_tag:
                    try:
                        war = await self.api.get_current_war(clan_tag)
                    except aiohttp.ClientResponseError as err:
                        if err.status not in (403, 404):
                            raise

                wars[player_tag] = war

            return {
                "players": players,
                "wars": wars,
            }
        except Exception as err:
            raise UpdateFailed(f"Error fetching Clash of Clans data: {err}") from err