from datetime import datetime, timezone

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for player_tag in coordinator.player_tags:
        entities.extend(
            [
                ClashPlayerInfoSensor(coordinator, player_tag),
                ClashPlayerTrophiesSensor(coordinator, player_tag),
                ClashPlayerTownHallLevelSensor(coordinator, player_tag),
                ClashPlayerBuilderHallLevelSensor(coordinator, player_tag),
                ClashPlayerExperienceLevelSensor(coordinator, player_tag),
                ClashPlayerDonationsSensor(coordinator, player_tag),
                ClashPlayerDonationsReceivedSensor(coordinator, player_tag),
                ClashCurrentWarAttacksRemainingSensor(coordinator, player_tag),
                ClashCurrentWarEndTimeSensor(coordinator, player_tag),
                ClashCurrentWarStartTimeSensor(coordinator, player_tag),
                ClashCurrentWarStateSensor(coordinator, player_tag),
            ]
        )

    async_add_entities(entities)


class ClashPlayerBaseSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator)
        self._player_tag = player_tag

    @property
    def _player(self):
        return self.coordinator.data.get("players", {}).get(self._player_tag, {})

    @property
    def device_info(self):
        player_name = self._player.get("name")
        device_name = player_name or f"Clash of Clans ({self._player_tag})"

        return DeviceInfo(
            identifiers={(DOMAIN, self._player_tag)},
            name=device_name,
            manufacturer="Supercell",
            model="Clash of Clans",
        )

    @property
    def _war(self):
        return self.coordinator.data.get("wars", {}).get(self._player_tag) or {}

    def _parse_coc_time(self, value: str | None):
        if not value:
            return None

        try:
            return datetime.strptime(value, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc)
        except ValueError:
            return None


class ClashPlayerInfoSensor(ClashPlayerBaseSensor):
    """Sensor for Clash of Clans player info."""

    _attr_name = "Info"
    _attr_icon = "mdi:information"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_info"

    @property
    def native_value(self):
        return self._player.get("name")
    
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

    _attr_name = "Trophies"
    _attr_icon = "mdi:trophy"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_trophies"

    @property
    def native_value(self):
        return self._player.get("trophies")

class ClashPlayerTownHallLevelSensor(ClashPlayerBaseSensor):
    _attr_name = "Town Hall Level"
    _attr_icon = "mdi:home"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_town_hall_level"

    @property
    def native_value(self):
        return self._player.get("townHallLevel")


class ClashPlayerBuilderHallLevelSensor(ClashPlayerBaseSensor):
    _attr_name = "Builder Hall Level"
    _attr_icon = "mdi:home-variant"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_builder_hall_level"

    @property
    def native_value(self):
        return self._player.get("builderHallLevel")


class ClashPlayerExperienceLevelSensor(ClashPlayerBaseSensor):
    _attr_name = "Experience Level"
    _attr_icon = "mdi:star"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_xp_level"

    @property
    def native_value(self):
        return self._player.get("expLevel")


class ClashPlayerDonationsSensor(ClashPlayerBaseSensor):
    _attr_name = "Donations"
    _attr_icon = "mdi:hand-coin"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_donations"

    @property
    def native_value(self):
        return self._player.get("donations")


class ClashPlayerDonationsReceivedSensor(ClashPlayerBaseSensor):
    _attr_name = "Donations Received"
    _attr_icon = "mdi:hand-heart"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_donations_received"

    @property
    def native_value(self):
        return self._player.get("donationsReceived")


class ClashCurrentWarAttacksRemainingSensor(ClashPlayerBaseSensor):
    _attr_name = "War Attacks Remaining"
    _attr_icon = "mdi:sword-cross"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_war_attacks_remaining"

    @property
    def native_value(self):
        if self._war.get("state") != "inWar":
            return None

        attacks_per_member = self._war.get("attacksPerMember")
        if not isinstance(attacks_per_member, int):
            return None

        members = self._war.get("clan", {}).get("members", [])
        if not isinstance(members, list):
            return None

        member = next((m for m in members if m.get("tag") == self._player_tag), None)
        if not member:
            return None

        completed_attacks = member.get("attacks")
        if completed_attacks is None:
            completed_count = 0
        elif isinstance(completed_attacks, list):
            completed_count = len(completed_attacks)
        else:
            return None

        remaining = attacks_per_member - completed_count
        return max(0, remaining)


class ClashCurrentWarEndTimeSensor(ClashPlayerBaseSensor):
    _attr_name = "Current War End Time"
    _attr_icon = "mdi:flag-checkered"
    _attr_device_class = "timestamp"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_current_war_end_time"

    @property
    def native_value(self):
        return self._parse_coc_time(self._war.get("endTime"))

class ClashCurrentWarStartTimeSensor(ClashPlayerBaseSensor):
    _attr_name = "Current War Start Time"
    _attr_icon = "mdi:calendar-clock"
    _attr_device_class = "timestamp"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_current_war_start_time"

    @property
    def native_value(self):
        return self._parse_coc_time(self._war.get("startTime"))

class ClashCurrentWarStateSensor(ClashPlayerBaseSensor):
    _attr_name = "Current War State"
    _attr_icon = "mdi:sword"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_current_war_state"

    @property
    def native_value(self):
        return self._war.get("state")
