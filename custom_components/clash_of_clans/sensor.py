from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            ClashPlayerTrophiesSensor(coordinator),
            ClashPlayerBestTrophiesSensor(coordinator),
            ClashPlayerTownHallLevelSensor(coordinator),
            ClashPlayerBuilderHallLevelSensor(coordinator),
            ClashPlayerExperienceLevelSensor(coordinator),
            ClashPlayerWarStarsSensor(coordinator),
            ClashPlayerDonationsSensor(coordinator),
            ClashPlayerDonationsReceivedSensor(coordinator),
        ]
    )


class ClashPlayerBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def _player(self):
        return self.coordinator.data.get("player", {})

    @property
    def device_info(self):
        player_name = self._player.get("name")
        device_name = player_name or f"Clash of Clans ({self.coordinator.player_tag})"

        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.player_tag)},
            name=device_name,
            manufacturer="Supercell",
            model="Clash of Clans",
        )


class ClashPlayerInfoSensor(ClashPlayerBaseSensor):
    """Sensor for Clash of Clans player info."""

    _attr_name = "Player Info"
    _attr_icon = "mdi:information"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.player_tag}_info"

    @property
    def native_value(self):
        return self.coordinator.data["player"]["name"]
    
    @property
    def extra_state_attributes(self):
        player = self._player

        return {
            "league": player.get("leagueTier", {}).get("name"),
            "best_trophies": player.get("bestTrophies"),
            "builder_hall": player.get("builderHallLevel"),
            "experience_level": player.get("expLevel"),
            "clan_capital_contributions": player.get("clanCapitalContributions"),
            "clan_tag": player.get("clan", {}).get("tag"),
            "clan_name": player.get("clan", {}).get("name"),
        }

class ClashPlayerTrophiesSensor(ClashPlayerBaseSensor):
    """Sensor for Clash of Clans player trophies."""

    _attr_name = "Player Trophies"
    _attr_icon = "mdi:trophy"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.player_tag}_trophies"

    @property
    def native_value(self):
        return self.coordinator.data["player"]["trophies"]

class ClashPlayerTownHallLevelSensor(ClashPlayerBaseSensor):
    _attr_name = "Town Hall Level"
    _attr_icon = "mdi:home"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.player_tag}_town_hall_level"

    @property
    def native_value(self):
        return self._player.get("townHallLevel")


class ClashPlayerBuilderHallLevelSensor(ClashPlayerBaseSensor):
    _attr_name = "Builder Hall Level"
    _attr_icon = "mdi:home-variant"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.player_tag}_builder_hall_level"

    @property
    def native_value(self):
        return self._player.get("builderHallLevel")


class ClashPlayerExperienceLevelSensor(ClashPlayerBaseSensor):
    _attr_name = "Experience Level"
    _attr_icon = "mdi:star"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.player_tag}_xp_level"

    @property
    def native_value(self):
        return self._player.get("expLevel")


class ClashPlayerDonationsSensor(ClashPlayerBaseSensor):
    _attr_name = "Clash of Clans Player Donations"
    _attr_icon = "mdi:hand-coin"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.player_tag}_donations"

    @property
    def native_value(self):
        return self._player.get("donations")


class ClashPlayerDonationsReceivedSensor(ClashPlayerBaseSensor):
    _attr_name = "Clash of Clans Player Donations Received"
    _attr_icon = "mdi:hand-heart"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.player_tag}_donations_received"

    @property
    def native_value(self):
        return self._player.get("donationsReceived")
