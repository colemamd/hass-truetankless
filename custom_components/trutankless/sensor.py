"""Support for TruTankless water heaters."""
import logging

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    COORDINATOR,
    DOMAIN,
    INCOMING_VOLTAGE,
    INLET_TEMPERATURE,
    OUTLET_TEMPERATURE,
    PCB_TEMP,
    SENSORS,
    TEMPERATURE_SET_POINT,
    TOTAL_FLOW,
)

_LOGGER = logging.getLogger(__name__)

SENSOR_NAMES_TO_ATTRIBUTES = {
    INLET_TEMPERATURE: "inlet_temperature",
    OUTLET_TEMPERATURE: "outlet_temperature",
    TEMPERATURE_SET_POINT: "temperature_set_point",
    TOTAL_FLOW: "total_flow",
    INCOMING_VOLTAGE: "incoming_voltage",
    PCB_TEMP: "pcb_temp",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TruTankless sensor based on a config entry."""
    data: dict = hass.data[DOMAIN][entry.entry_id]
    coordinator: DataUpdateCoordinator = data[COORDINATOR]
    device_data: dict = coordinator.data

    entities: list[TruTanklessSensor] = []
    for description in SENSORS:
        entities.append(TruTanklessSensor(coordinator, description, device_data))

    async_add_entities(entities)


class TruTanklessSensor(CoordinatorEntity, SensorEntity):
    """Define a TruTankless sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
        device_data,
    ) -> None:
        """Initialize TruTankless Sensor."""
        self.device_data = device_data
        self.entity_description = description
        self._name = self.entity_description.name
        super().__init__(coordinator)

        self._attr_unique_id = f"{self.device_id} {self.entity_description.key}"

    @property
    def native_value(self):
        """Return the value of the sensor."""
        value = getattr(self.coordinator.data, self.entity_description.key)
        return value

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.serial_number)},
            manufacturer="TruTankless",
            model=self.model,
            name=self.label,
        )

    @property
    def device_id(self):
        """Return the device id of the device."""
        return getattr(self.device_data, "device_id")

    @property
    def label(self):
        """Return the label of the device."""
        return getattr(self.device_data, "label")

    @property
    def location_id(self):
        """Return the location id."""
        return getattr(self.device_data, "location_id")

    @property
    def model(self):
        """Return the model number of the device."""
        return getattr(self.device_data, "model")

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def serial_number(self):
        """Return the serial number of the device."""
        return getattr(self.device_data, "serial_number")
