from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN, CONF_API_TOKEN, CONF_PLAYER_TAG, CONF_CLAN_TAG
from .api import ClashOfClansApi


class ClashOfClansConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Clash of Clans."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Prevent duplicates
            await self.async_set_unique_id(user_input[CONF_PLAYER_TAG])
            self._abort_if_unique_id_configured()

            api = ClashOfClansApi(user_input[CONF_API_TOKEN])

            try:
                # Validate player tag
                await api.get_player(user_input[CONF_PLAYER_TAG])
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                return self.async_create_entry(
                    title="Clash of Clans",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_TOKEN): str,
                    vol.Required(CONF_PLAYER_TAG): str,
                    vol.Required(CONF_CLAN_TAG): str,
                }
            ),
            errors=errors,
        )
