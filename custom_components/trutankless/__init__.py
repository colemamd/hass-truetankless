"""The trutankless integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_NAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pytrutankless.api import TruTanklessApiInterface
from pytrutankless.errors import TruTanklessError

from .const import COORDINATOR, DOMAIN, NAME, PLATFORMS

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=300)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up trutankless from a config entry."""

    config = entry.data
    email = config[CONF_EMAIL]
    password = config[CONF_PASSWORD]
    name = config[CONF_NAME]
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = {}

    api = await TruTanklessApiInterface.login(email, password)

    async def async_update_device_data():
        """Retrieve data from the API endpoint."""
        try:
            await api.get_devices()
            for dev in api.devices.keys():  # type: ignore
                data = await api.refresh_device(dev)
                _LOGGER.debug("Retrieved data from API: %s:", data)
        except TruTanklessError as err:
            raise UpdateFailed from err

        return data  # type: ignore

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN} device",
        update_method=async_update_device_data,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        COORDINATOR: coordinator,
        NAME: name,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
