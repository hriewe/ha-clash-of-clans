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
                ClashTroopProgressionSensor(coordinator, player_tag),
                ClashSpellProgressionSensor(coordinator, player_tag),
                ClashHeroProgressionSensor(coordinator, player_tag),
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

    def _progression(
        self,
        key: str,
        *,
        village: str | None = "home",
        exclude_names: set[str] | None = None,
        exclude_name_contains: set[str] | None = None,
    ):
        items = self._player.get(key, [])
        if not isinstance(items, list):
            return None, {}

        current_total = 0
        max_total = 0
        item_count = 0
        maxed_count = 0

        for item in items:
            if not isinstance(item, dict):
                continue
            if village is not None and item.get("village") != village:
                continue

            name = item.get("name")
            if isinstance(name, str):
                name_lower = name.lower()
                if exclude_names and name_lower in exclude_names:
                    continue
                if exclude_name_contains and any(s in name_lower for s in exclude_name_contains):
                    continue

            level = item.get("level")
            max_level = item.get("maxLevel")
            if not isinstance(level, int) or not isinstance(max_level, int) or max_level <= 0:
                continue

            item_count += 1
            current_total += level
            max_total += max_level
            if level >= max_level:
                maxed_count += 1

        if max_total <= 0 or item_count == 0:
            return None, {
                "village": village,
                "items": item_count,
                "items_maxed": maxed_count,
                "current_total": current_total,
                "max_total": max_total,
            }

        percent = (current_total / max_total) * 100
        return round(percent, 2), {
            "village": village,
            "items": item_count,
            "items_maxed": maxed_count,
            "current_total": current_total,
            "max_total": max_total,
        }


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


class ClashTroopProgressionSensor(ClashPlayerBaseSensor):
    _attr_name = "Troop/Pet Progression"
    _attr_icon = "mdi:sword"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = "measurement"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_troop_progression"

    @property
    def native_value(self):
        exclude_names = {
            "ice hound",
            "inferno dragon",
            "rocket balloon",
            "sneaky goblin",
        }
        value, _attrs = self._progression(
            "troops",
            village="home",
            exclude_names=exclude_names,
            exclude_name_contains={"super"},
        )
        return value

    @property
    def extra_state_attributes(self):
        exclude_names = {
            "ice hound",
            "inferno dragon",
            "rocket balloon",
            "sneaky goblin",
        }
        _value, attrs = self._progression(
            "troops",
            village="home",
            exclude_names=exclude_names,
            exclude_name_contains={"super"},
        )
        return attrs


class ClashSpellProgressionSensor(ClashPlayerBaseSensor):
    _attr_name = "Spell Progression"
    _attr_icon = "mdi:magic-staff"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = "measurement"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_spell_progression"

    @property
    def native_value(self):
        value, _attrs = self._progression("spells", village="home")
        return value

    @property
    def extra_state_attributes(self):
        _value, attrs = self._progression("spells", village="home")
        return attrs


class ClashHeroProgressionSensor(ClashPlayerBaseSensor):
    _attr_name = "Hero Progression"
    _attr_icon = "mdi:shield-sword"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = "measurement"

    def __init__(self, coordinator, player_tag: str):
        super().__init__(coordinator, player_tag)
        self._attr_unique_id = f"{DOMAIN}_{player_tag}_hero_progression"

    @property
    def native_value(self):
        value, _attrs = self._progression("heroes", village="home")
        return value

    @property
    def extra_state_attributes(self):
        _value, attrs = self._progression("heroes", village="home")
        return attrs


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
