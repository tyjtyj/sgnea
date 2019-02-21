"""
"""
import asyncio
import logging
import json
from datetime import timedelta, datetime


import aiohttp
import voluptuous as vol

import homeassistant.helpers.config_validation as cv


from homeassistant.exceptions import PlatformNotReady

from homeassistant.const import (
    CONF_NAME, CONF_RESOURCE, STATE_UNKNOWN)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.config_validation import PLATFORM_SCHEMA

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from homeassistant.components.sensor.rest import RestData

_LOGGER = logging.getLogger(__name__)

CONF_AREA = 'area'
DEFAULT_RESOURCE = 'https://api.data.gov.sg/v1/environment/2-hour-weather-forecast?date_time=' + datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
DEFAULT_NAME = 'SGNEA NowCast'
SCAN_INTERVAL = timedelta(minutes=5)
PARALLEL_UPDATES = 1

TIMEOUT = 10

CONDITION_DETAILS = {
    'BR': 'Mist',
    'CL': 'Cloudy',
    'DR': 'Drizzle',
    'FA': 'Fair (Day)',
    'FG': 'Fog',
    'FN': 'Fair (Night)',
    'FW': 'Fair & Warm',
    'HG': 'Heavy Thundery Showers with Gusty Winds',
    'HR': 'Heavy Rain',
    'HS': 'Heavy Showers',
    'HT': 'Heavy Thundery Showers',
    'HZ': 'Hazy',
    'LH': 'Slightly Hazy',
    'LR': 'Light Rain',
    'LS': 'Light Showers',
    'OC': 'Overcast',
    'PC': 'Partly Cloudy (Day)',
    'PN': 'Partly Cloudy (Night)',
    'PS': 'Passing Showers',
    'RA': 'Moderate Rain',
    'SH': 'Showers',
    'SK': 'Strong Winds, Showers',
    'SN': 'Snow',
    'SR': 'Strong Winds, Rain',
    'SS': 'Snow Showers',
    'SU': 'Sunny',
    'SW': 'Strong Winds',
    'TL': 'Thundery Showers',
    'WC': 'Windy, Cloudy',
    'WD': 'Windy',
    'WF': 'Windy, Fair',
    'WR': 'Windy, Rain',
    'WS': 'Windy, Showers',
}

INV_CONDITION_DETAILS = {v: k for k, v in CONDITION_DETAILS.items()}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_AREA): cv.string,
    vol.Optional(CONF_RESOURCE, default=DEFAULT_RESOURCE): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

@asyncio.coroutine
async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):

    """Set up the Web scrape sensor."""
    _LOGGER.info('SGNEAWEB loaded')
    name = config.get(CONF_NAME)
    resource = config.get(CONF_RESOURCE)
    area = config.get(CONF_AREA)

    method = 'GET'
    payload = None
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    verify_ssl = 0
    auth = None

    try:
        rest = RestData(method, resource, auth, headers, payload, verify_ssl)
        rest.update()
    except (aiohttp.client_exceptions.ClientConnectorError,
            asyncio.TimeoutError):
        _LOGGER.exception('Failed to connect to servers.')
        raise PlatformNotReady
    async_add_entities([NeaSensorWeb(rest, name, area)], True)       


class NeaSensorWeb(Entity):
    """Representation of a web scrape sensor."""

    def __init__(self, rest, name, area):
        """Initialize a web scrape sensor."""
        self.rest = rest
        self._name = name
        self.area = area
        self._state = STATE_UNKNOWN
        self._picurl = STATE_UNKNOWN

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def entity_picture(self):
        """Return the entity picture to use in the frontend, if any."""
        return self._picurl

    @property             
    def state(self):
        """Return the state of the device."""
        return self._state

    #@Throttle(SCAN_INTERVAL)
    @asyncio.coroutine
    async def async_update(self):

        try:
            self.rest.update()
            json_dict = json.loads(self.rest.data)
            forecasts = json_dict['items'][0]['forecasts']

            for entry in forecasts:
              if entry['area'] == self.area:
                value = entry['forecast']
                break
            if value is not None:
                self._picurl = 'https://www.nea.gov.sg/assets/images/icons/weather-bg/' + INV_CONDITION_DETAILS[value] + '.png';
                _LOGGER.debug('PicsURL : %s',self._picurl)
            else:
                value = 'No Data'

            if value is None:
                _LOGGER.error("Unable to fetch data from %s", value)
                return False
        except (aiohttp.client_exceptions.ClientConnectorError,
                asyncio.TimeoutError,KeyError):
            _LOGGER.error("Error. The data value is: %s", self.rest.data)
            return False
        _LOGGER.debug("The data value is: %s", self.rest.data)
        #self._state = CONDITION_DETAILS[self._picurl]
        self._state = value.strip()
		
