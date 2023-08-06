import logging

from .danfossallyapi import *

_LOGGER = logging.getLogger(__name__)

__version__ = '0.0.23'


class DanfossAlly:
    """Danfoss Ally API connector."""

    def __init__(self):
        """Init the API connector variables."""
        self._authorized = False
        self._token = None
        self.devices = {}

        self._api = DanfossAllyAPI()

    def initialize(self, key, secret):
        """Authorize and initialize the connection."""

        token = self._api.getToken(key, secret)
        
        if token is False:
            self._authorized = False
            _LOGGER.error("Error in authorization")
            return False

        _LOGGER.debug("Token received: %s",
                      self._api.token)
        self._token = self._api.token
        self._authorized = True
        return self._authorized

    def getDeviceList(self):
        """Get device list."""
        devices = self._api.get_devices()

        if devices is None:
            _LOGGER.error("No devices loaded, API error?!")
            return

        if not devices:
            _LOGGER.error("No devices loaded, API connection error?!")
            return

        if not 'result' in devices:
            _LOGGER.error("Something went wrong loading devices!")
            return

        for device in devices['result']:
            self.devices[device['id']] = {}
            self.devices[device['id']]['isThermostat'] = False
            self.devices[device['id']]['name'] = device['name'].strip()
            self.devices[device['id']]['online'] = device['online']
            self.devices[device['id']]['update'] = device['update_time']
            if 'model' in device:
                self.devices[device['id']]['model'] = device['model']
            for status in device['status']:
                if status['code'] == 'temp_set':
                    setpoint = float(status['value'])
                    setpoint = setpoint/10
                    self.devices[device['id']]['setpoint'] = setpoint
                    self.devices[device['id']]['isThermostat'] = True
                elif status['code'] == 'temp_current':
                    temperature = float(status['value'])
                    temperature = temperature/10
                    self.devices[device['id']]['temperature'] = temperature
                elif status['code'] == 'upper_temp':
                    temperature = float(status['value'])
                    temperature = temperature/10
                    self.devices[device['id']]['upper_temp'] = temperature
                elif status['code'] == 'lower_temp':
                    temperature = float(status['value'])
                    temperature = temperature/10
                    self.devices[device['id']]['lower_temp'] = temperature
                elif status['code'] == 'battery_percentage':
                    battery = status['value']
                    self.devices[device['id']]['battery'] = battery
                elif status['code'] == 'window_state':
                    window = status['value']
                    if window == "open":
                        self.devices[device['id']]['window_open'] = True
                    else:
                        self.devices[device['id']]['window_open'] = False
                elif status['code'] == 'child_lock':
                    childlock = status['value']
                    self.devices[device['id']]['child_lock'] = childlock
                elif status['code'] == 'mode':
                    self.devices[device['id']]['mode'] = status['value']


    def getDevice(self, device_id):
        """Get device data."""
        device = self._api.get_device(device_id)

    @property
    def authorized(self):
        """Return authorized status."""
        return self._authorized

    def setTemperature(self, device_id: str, temp: float) -> bool:
        """Updates temperature setpoint for given device."""
        temperature = int(temp*10)

        result = self._api.set_temperature(device_id, temperature)

        return result