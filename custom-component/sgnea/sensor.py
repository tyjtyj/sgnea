import logging
import json
import time
import voluptuous as vol
from datetime import timedelta
from requests import Session
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME, CONF_RESOURCE, STATE_UNKNOWN)
from homeassistant.helpers.entity import Entity
from homeassistant.exceptions import PlatformNotReady
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_AREA = 'area'
DEFAULT_RESOURCE = 'https://www.nea.gov.sg/api/WeatherForecast/forecast24hrnowcast2hrs/' 
DEFAULT_NAME = 'SGNEA NowCast'
DEFAULT_TIMEOUT = 10
SCAN_INTERVAL = timedelta(minutes=5)
PARALLEL_UPDATES = 1
TIMEOUT = 10

CONDITION_DETAILS = {
    'BR': 'Mist',
    'CL': 'Cloudy',
    'DR': 'Drizzle',
    'FA': 'Fair',
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
    'PC': 'Partly Cloudy',
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
    resourcenow = resource +  str(time.time())[:8] + '00'
    auth = None
    rest = NEARestData(method, resourcenow, auth, headers, payload, verify_ssl)
    try:
        rest.update()
    except:
        _LOGGER.error("Unable to fetch data from %s", resourcenow)        
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
        try: 
            resourcenow = self._resource +  str(time.time())[:8] + '00'
            rest = NEARestData('GET', resourcenow, None, self._headers, None, 0)
            rest.update()
            json_dict = json.loads(rest.data)
            forecasts = json_dict['Channel2HrForecast']['Item']['WeatherForecast']['Area']
            for entry in forecasts:
                if entry['Name'] == self._area:
                    value = CONDITION_DETAILS[entry['Forecast']]
                    break
            self._state = value.strip()
            if value is not None:
                self._picurl = 'https://www.nea.gov.sg/assets/images/icons/weather-bg/' + INV_CONDITION_DETAILS[value] + '.png';
                _LOGGER.debug('PicsURL : %s',self._picurl)
            else:
                value = STATE_UNKNOWN
                _LOGGER.error("Unable to fetch data from %s", value)
                return False
        except:
            _LOGGER.error("Error. The data value is: %s", forecasts)
            return
        _LOGGER.debug("The data value is: %s", rest.data)
        
class NEARestData:
    """Class for handling the data retrieval."""

    def __init__(
        self, method, resource, auth, headers, data, verify_ssl, timeout=DEFAULT_TIMEOUT
    ):
        """Initialize the data object."""
        self._method = method
        self._resource = resource
        self._auth = auth
        self._headers = headers
        self._request_data = data
        self._verify_ssl = verify_ssl
        self._timeout = timeout
        self._http_session = Session()
        self.data = None
        self.headers = None

    def __del__(self):
        """Destroy the http session on destroy."""
        self._http_session.close()

    def set_url(self, url):
        """Set url."""
        self._resource = url

    def update(self):
        """Get the latest data from REST service with provided method."""
        _LOGGER.debug("Updating from %s", self._resource)
        try:
            response = self._http_session.request(
                self._method,
                self._resource,
                headers=self._headers,
                auth=self._auth,
                data=self._request_data,
                timeout=self._timeout,
                verify=self._verify_ssl,
            )
            self.data = response.text
            self.headers = response.headers
        except requests.exceptions.RequestException as ex:
            _LOGGER.error("Error fetching data: %s failed with %s", self._resource, ex)
            self.data = None
            self.headers = None
