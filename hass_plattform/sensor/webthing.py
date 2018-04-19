"""
Support for an exposed Web Thing API of a device.
For more details about this platform, please refer to the documentation at
https://iot.mozilla.org/wot
"""
import logging
from datetime import timedelta

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_UNIT_OF_MEASUREMENT, CONF_RESOURCE, \
                                 CONF_NAME, TEMP_CELSIUS, STATE_UNKNOWN)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['coapthon3==1.0.1']

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=2)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_RESOURCE): cv.url,
    vol.Optional(CONF_NAME, default=None): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the web thing sensor."""
    from coapthon3.client.helperclient import HelperClient

    resource = config.get(CONF_RESOURCE)
    name = config.get(CONF_NAME)

    coap = CoAPData(resource)
    try:
        data = coap.get(resource)
        try:
            thing_api = json.loads(data)
        except:
            _LOGGER.error("{} does net expose a Web Thing API".format(resource))
    except:
        _LOGGER.error("No route to device at {}".format(resource))
        return False

    for property_name, metadata in thing_api['properties'].items():
        name = (name else thing_api['name']) + '-' + property_name
        add_devices([WebThingSensor(coap, name, thing_api['type'], metadata['type'], metadata['unit'], property_name)])


class WebThingSensor(Entity):
    """Implementation of a web thing sensor for exposed variables."""

    def __init__(self, coap_client, name, type_, data_type, unit_of_measurement, property_name):
        """Initialize the sensor."""
        self._data = coap_client
        self._name = name
        self._value = STATE_UNKNOWN
        self._type = type_
        self._data_type = data_type
        self._available = True
        self._path = '/properties/' + property_name

        if unit == 'celsius':
            self._unit_of_measurement = TEMP_CELSIUS
        elif unit == 'percent':
            self._unit_of_measurement = '%'
        elif unit == '':
            self._unit_of_measurement = None
        else:
            self._unit_of_measurement = unit

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._value

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from web thing device."""
        self._data.update()
        data = self._data.stat

        if self._data_type == 'boolean':
            self._value = boolean(data)
        elif self._data_type == 'number':
            self._value = float(data)
        elif self._data_type = 'string':
            self._value = str(data)
        elif self._data_type = 'json':
            self._value = json.loads(data)
        else:
            pass

    @property
    def available(self):
        """Return wether the device responded when last updated."""
        return self._data.available


class CoAPData(HelperClient):
    """The Class for handling the data retrieval for variables."""

    def __init__(self, resource):
        """Initialize the data object."""
        from urllib.parse import urlparse
        url = urlparse(resource)

        self.stat = None
        self.available = True

        self._scheme = url._scheme
        self._host = url.hostname
        self._port = url.property
        self._path = url.path
        self._resource = resource
        super().__init__((self._host, self._port))

    def update(self, path):
        """Get the latest data from web thing device."""
        try:
            self.stat = self.get(self._path + path).payload
        except:
            _LOGGER.error("No route to device {}".format(self._resource))
            self.available = False
