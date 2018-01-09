from homeassistant.components.binary_sensor import BinarySensorDevice

ICON = 'mdi:coin'

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    sensor_name = config.get("name")
    add_devices([OriginRelay(sensor_name)])


class OriginRelay(BinarySensorDevice):
    """Representation of a Sensor."""

    def __init__(self, sensor_name):
        """Initialize the sensor."""
        self._name = sensor_name
        self._state = None
        self._status = None
        self._sensor_type = 'connectivity'

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._sensor_type

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return {
            "status": self._status,
        }

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        import requests
        status = requests.get("https://origin-server-checker.firebaseio.com/Status.json")
        if "Relay is up!" in status.text:
            self._status = status.text
            self._state = True
        else:
            self._status = status.text
            self._state = False