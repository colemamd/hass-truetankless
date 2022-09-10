"""Support for TruTankless water heaters."""

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import COORDINATOR, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TruTankless water heater based on a config entry."""
    data: dict = hass.data[DOMAIN][entry.entry_id]
    coordinator: DataUpdateCoordinator = data[COORDINATOR]
    device_data: dict = coordinator.data

    entities: list[TruTanklessWaterHeater] = []
    entities.append(TruTanklessWaterHeater(device_data))

    async_add_entities(entities)


class TruTanklessWaterHeater(WaterHeaterEntity):
    """Define a TruTankless water heater."""

    _attr_has_entity_name: bool = True

    def __init__(self, water_heater):
        """Initialize a TruTankless water heater."""
        self.water_heater = water_heater
        self._attr_unique_id: str = self.serial_number
        self._name = self.label

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry info for device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.serial_number)},
            manufacturer="TruTankless",
            model=self.model,
            name=self.name,
        )

    @property
    def current_temperature(self) -> str:
        """Return the current outlet temperature."""
        return getattr(self.water_heater, "outlet_temperature")

    @property
    def is_away_mode_on(self) -> bool:
        """Return True if vacation setting is on."""
        return getattr(self.water_heater, "vacation_setting")

    @property
    def is_eco_setting_on(self) -> bool:
        """Return True if eco setting is on."""
        return getattr(self.water_heater, "eco_setting")

    @property
    def label(self) -> str:
        """Return the label of the device."""
        return getattr(self.water_heater, "label")

    @property
    def model(self) -> str:
        """Return the model of the device."""
        return getattr(self.water_heater, "model")

    @property
    def name(self) -> str:
        """Return the name of the water heater."""
        return self._name

    @property
    def serial_number(self) -> str:
        """Return the serial number of the device."""
        return getattr(self.water_heater, "serial_number")

    @property
    def supported_features(self):
        """Return the supported features."""
        return (
            WaterHeaterEntityFeature.AWAY_MODE
            | WaterHeaterEntityFeature.TARGET_TEMPERATURE
        )

    @property
    def target_temperature(self) -> float:
        """Return the target temperature."""
        return getattr(self.water_heater, "temperature_set_point")

    @property
    def temperature_unit(self):
        """Return the temp units provided by the device."""
        return TEMP_CELSIUS
