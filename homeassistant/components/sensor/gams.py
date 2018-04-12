"""
Support for GAMS air quality .

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.gams/
"""
from logging import getLogger
from homeassistant.components.sensor import PLATFORM_SCHEMA

import voluptuous as vol
from homeassistant.const import CONF_ID, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity


# REQUIREMENTS = ['pygamsapi==1.0.0']
REQUIREMENTS = ['pyairvisual==1.0.0']


_LOGGER = getLogger(__name__)


DEFAULT_NAME = 'GAMS Platform Sensor'

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ID): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup GAMS platform."""
    import pygamsapi

    uuid = config.get(CONF_ID)

    gams_platform = pygamsapi.GamsClient()

    # TODO: add check if platform was created

    add_devices([GamsSensor(gams_platform, uuid)])


class GamsSensor(Entity):
    """Define a sensor."""

    def __init__(self, gams_platform, uuid):
        self.gams_platform = gams_platform
        self.uuid = uuid
        self.latest = {}

        self._state = None
        self._unit_of_measurement = 'PM2.5'


    @property
    def name(self):
        """Return name if the sensor"""
        return '{}'.format(self.uuid)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'PM2.5'

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.gams_platform.latest(self.uuid)['fields']['pm25']
