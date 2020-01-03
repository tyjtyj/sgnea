import logging
import json
import time
import voluptuous as vol
from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.rest.sensor import RestData

from homeassistant.const import (
    CONF_NAME, CONF_RESOURCE, STATE_UNKNOWN)
from homeassistant.helpers.entity import Entity
from homeassistant.exceptions import PlatformNotReady
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_AREA = 'area'
DEFAULT_RESOURCE = 'https://www.nea.gov.sg/api/WeatherForecast/forecast24hrnowcast2hrs/' 
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

def setup_platform(hass, config, add_entities,
                               discovery_info=None):
    """Set up the Web scrape sensor."""
    _LOGGER.info('SGNEAWEB loaded')
    name = config.get(CONF_NAME)
    resource = config.get(CONF_RESOURCE)
    method = 'GET'
    payload = None
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    verify_ssl = 0
    area = config.get(CONF_AREA)
    resourcenow = resource +  str(time.time())
    auth = None
    rest = RestData(method, resourcenow, auth, headers, payload, verify_ssl)
    
    rest.update()

    if rest.data is None:
        raise PlatformNotReady

    add_entities([NeaSensorWeb(name, resource, headers, area)], True)       
																			 
					  


class NeaSensorWeb(Entity):
    """Representation of a web scrape sensor."""

    def __init__(self, name, resource, headers, area):
        """Initialize a web scrape sensor."""

        self._name = name
        self._area = area
        self._resource = resource
        self._headers = headers
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

    def update(self):
        """Get the latest data from the source and updates the state."""
        resourcenow = self._resource +  str(time.time()) 
        rest = RestData('GET', resourcenow, None, self._headers, None, 0)
        rest.update()
        try: 
            json_dict = json.loads(rest.data)
            forecasts = json_dict['Channel2HrForecast']['Item']['WeatherForecast']['Area']
            for entry in forecasts:
                if entry['Name'] == self._area:
                    value = CONDITION_DETAILS[entry['Forecast']]
                    break

            if value is not None:
                self._picurl = 'https://www.nea.gov.sg/assets/images/icons/weather-bg/' + INV_CONDITION_DETAILS[value] + '.png';
                _LOGGER.debug('PicsURL : %s',self._picurl)
            else:
                value = STATE_UNKNOWN
                _LOGGER.error("Unable to fetch data from %s", value)
                return False
        except (TimeoutError,KeyError):
            _LOGGER.error("Error. The data value is: %s", forecasts)
            return
        _LOGGER.debug("The data value is: %s", rest.data)
        self._state = value.strip()
