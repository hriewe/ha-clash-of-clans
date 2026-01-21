from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN, CONF_API_TOKEN, CONF_PLAYER_TAG, CONF_PLAYER_TAGS
from .api import ClashOfClansApi


def _parse_player_tags(value: str) -> list[str]:
    raw = value.replace("\n", ",")
    tags = [t.strip() for t in raw.split(",") if t.strip()]
    return tags


class ClashOfClansConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Clash of Clans."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            tags = _parse_player_tags(user_input[CONF_PLAYER_TAGS])
            if not tags:
                errors["base"] = "cannot_connect"

            # Prevent duplicates (order-independent)
            unique_id = ",".join(sorted(tags))
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            api = ClashOfClansApi(user_input[CONF_API_TOKEN])

            try:
                # Validate player tags
                for tag in tags:
                    await api.get_player(tag)
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                return self.async_create_entry(
                    title="Clash of Clans",
                    data={
                        CONF_API_TOKEN: user_input[CONF_API_TOKEN],
                        CONF_PLAYER_TAGS: tags,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_TOKEN): str,
                    vol.Required(CONF_PLAYER_TAGS): str,
                }
            ),
            errors=errors,
        )
