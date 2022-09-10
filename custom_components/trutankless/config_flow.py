"""Config flow for trutankless integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_NAME, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
from pytrutankless.api import TruTanklessApiInterface
from pytrutankless.errors import TruTanklessError

from .const import DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DOMAIN): str,
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class TruTanklessFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for trutankless."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.data_schema = STEP_USER_DATA_SCHEMA
        self.location_id: str
        self.unique_id: str
        self.user_id: str

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            errors = {}
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            try:
                device = TruTanklessApiInterface()
                api = await device.login(email=email, password=password)
            except TruTanklessError:
                errors["base"] = "cannot_connect"
            else:
                self.user_id = api.user_id
                await self.async_set_unique_id(self.user_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)
