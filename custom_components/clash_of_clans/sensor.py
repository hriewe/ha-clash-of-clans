from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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

    @property
    def native_value(self):
        return self.coordinator.data["player"]["trophies"]
