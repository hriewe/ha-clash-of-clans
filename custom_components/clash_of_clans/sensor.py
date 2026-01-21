from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            ClashPlayerTrophiesSensor(coordinator),
        ]
    )


class ClashPlayerTrophiesSensor(CoordinatorEntity, SensorEntity):
    """Sensor for Clash of Clans player trophies."""

    _attr_name = "Clash of Clans Player Trophies"
    _attr_icon = "mdi:trophy"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.player_tag}_trophies"

        # Device Info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.player_tag)},
            name=f"Clash of Clans ({coordinator.player_tag})",
            manufacturer="Supercell",
            model="Clash of Clans",
        )

    @property
    def native_value(self):
        return self.coordinator.data["player"]["trophies"]
    
    @property
    def extra_state_attributes(self):
        player = self.coordinator.data["player"]

        return {
            "town_hall_level": player.get("townHallLevel"),
            "xp_level": player.get("expLevel"),
            "league": player.get("leagueTier", {}).get("name"),
            "best_trophies": player.get("bestTrophies"),
            "war_stars": player.get("warStars"),
        }
