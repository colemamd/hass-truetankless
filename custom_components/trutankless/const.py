"""Constants for the trutankless integration."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import ATTR_VOLTAGE, TEMP_CELSIUS, VOLUME_GALLONS, Platform

COORDINATOR = "coordinator"
DOMAIN = "trutankless"
DEVICE = "device"
NAME = "name"
PLATFORMS = [Platform.SENSOR, Platform.WATER_HEATER]

INLET_TEMPERATURE = "inlet_temperature"
OUTLET_TEMPERATURE = "outlet_temperature"
TEMPERATURE_SET_POINT = "temperature_set_point"
TOTAL_FLOW = "total_flow"
INCOMING_VOLTAGE = "incoming_voltage"
PCB_TEMP = "pcb_temp"

SENSORS = (
    SensorEntityDescription(
        key="inlet_temperature",
        name="Inlet Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key="outlet_temperature",
        name="Outlet Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key="temperature_set_point",
        name="Temperature Set Point",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key="total_flow",
        name="Cumulative Flow",
        native_unit_of_measurement=VOLUME_GALLONS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="incoming_voltage",
        name="Incoming Voltage",
        native_unit_of_measurement=ATTR_VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    SensorEntityDescription(
        key="pcb_temp",
        name="PCB Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
)
