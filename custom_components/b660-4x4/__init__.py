import logging

import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_IP_ADDRESS,
    CONF_PORT,
    CONF_NAME,
)
from homeassistant.helpers.entity_component import EntityComponent
from .telnet_client import TelnetClient
from .const import DOMAIN
from homeassistant.helpers.entity import Entity
from datetime import timedelta

# Constants for your integration
_LOGGER = logging.getLogger(__name__)
ENTITY_ID_FORMAT = DOMAIN + ".{}"

# Configuration schema if needed
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Required(CONF_IP_ADDRESS): cv.string,
                vol.Required(CONF_PORT, default=23): cv.port,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the component."""
    conf = config[DOMAIN]
    username = conf[CONF_USERNAME]
    password = conf[CONF_PASSWORD]
    ip = conf[CONF_IP_ADDRESS]
    port = conf[CONF_PORT]

    telnet_client = TelnetClient(ip, port, username, password)

    hass.data[DOMAIN] = HDMIMatrix(telnet_client)

    try:
        await hass.async_add_executor_job(telnet_client.connect())
    except Exception as e:
        _LOGGER.error("Could not connect to Telnet server: %s", e)
        return False

    # Now, add your entity to the component
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform("sensor", DOMAIN, {}, config)
    )

    async def handle_switch_input(call):
        inp = call.data.get("input")
        output = call.data.get("output")
        device = hass.data[DOMAIN]
        await device.switch_input(inp, output)

    async def handle_set_cec_power(call):
        val = call.data.get("value")
        device = hass.data[DOMAIN]
        await device.set_CEC_power(val)

    async def handle_set_cec_auto_power(call):
        val = call.data.get("value")
        device = hass.data[DOMAIN]
        await device.set_CEC_auto_power(val)

    async def handle_set_power_delay_time(call):
        val = call.data.get("value")
        device = hass.data[DOMAIN]
        await device.set_CEC_power_delay_time(val)

    async def handle_set_hdcp_support(call):
        val = call.data.get("value")
        device = hass.data[DOMAIN]
        await device.set_HDCP_support(val)

    async def handle_set_input_edid(call):
        val = call.data.get("value")
        device = hass.data[DOMAIN]
        await device.set_input_EDID(val)

    async def handle_set_mute(call):
        val = call.data.get("value")
        device = hass.data[DOMAIN]
        await device.set_mute(val)

    hass.services.async_register(DOMAIN, "switch_input", handle_switch_input)
    hass.services.async_register(DOMAIN, "set_cec_power", handle_set_cec_power)
    hass.services.async_register(
        DOMAIN, "set_cec_auto_power", handle_set_cec_auto_power
    )
    hass.services.async_register(
        DOMAIN, "set_power_delay_time", handle_set_power_delay_time
    )
    hass.services.async_register(
        DOMAIN, "handle_set_hdcp_support", handle_set_hdcp_support
    )
    hass.services.async_register(DOMAIN, "set_input_edid", handle_set_input_edid)
    hass.services.async_register(DOMAIN, "set_mute", handle_set_mute)

    return True


class HDMIMatrix:
    def __init__(self, telnet_client):
        self.states = {
            "input1": 1,
            "input2": 2,
            "input3": 3,
            "input4": 4,
            "out1CECPower": False,
            "out2CECPower": False,
            "out3CECPower": False,
            "out4CECPower": False,
            "out1CECAutoPower": False,
            "out2CECAutoPower": False,
            "out3CECAutoPower": False,
            "out4CECAutoPower": False,
            "out1CECPowerDelayTime": 2,
            "out2CECPowerDelayTime": 2,
            "out3CECPowerDelayTime": 2,
            "out4CECPowerDelayTime": 2,
            "in1HDCPSupport": False,
            "in2HDCPSupport": False,
            "in3HDCPSupport": False,
            "in4HDCPSupport": False,
            "in1EDID": 17,
            "in2EDID": 17,
            "in3EDID": 17,
            "in4EDID": 17,
            "hdmi1Mute": False,
            "hdmi2Mute": False,
            "spdif1Mute": False,
            "spdif2Mute": False,
            "audio1Mute": False,
            "audio2Mute": False,
        }

        self.name = "HDMI Matrix"

        self.client = telnet_client

    def add_state_change_callback(self, callback):
        self._state_change_callback = callback

    async def switch_input(self, inp, output):
        inp = int(inp)
        if inp < 1 or inp > 4 or output < 1 or output > 4:
            logging.error("Incorrect params")
            return

        success = self.client.switch_input(inp, output)
        logging.info(f"SWITCHING INPUT {inp} {output}")
        if success:
            keys = ["input1", "input2", "input3", "input4"]
            self.update_state_on_success(keys, inp, output)
        else:
            logging.error("SWITCHING INPUT FAILED")

    async def set_CEC_power(self, out, val):
        if out < 1 or out > 4 or not val.isinstance(bool):
            logging.error("Incorrect params")
            return

        success = self.client.set_CEC_power(out, val)
        if success:
            keys = ["out1CECPower", "out2CECPower", "out3CECPower", "out4CECPower"]
            self.update_state_on_success(keys, out, val)
        else:
            logging.error("SET CEC POWER FAILED")

    async def set_CEC_auto_power(self, out, val):
        if out < 1 or out > 4 or not val.isinstance(bool):
            logging.error("Incorrect params")
            return

        success = self.client.set_CEC_auto_power(out, val)
        if success:
            keys = [
                "out1CECAutoPower",
                "out2CECAutoPower",
                "out3CECAutoPower",
                "out4CECAutoPower",
            ]
            self.update_state_on_success(keys, out, val)
        else:
            logging.error("SET CEC AUTO POWER FAILED")

    async def set_CEC_power_delay_time(self, out, val):
        if out < 1 or out > 4 or not val.isinstance(bool):
            logging.error("Incorrect params")
            return

        success = self.client.set_CEC_power_delay_time(out, val)
        if success:
            keys = [
                "out1CECPowerDelayTime",
                "out2CECPowerDelayTime",
                "out3CECPowerDelayTime",
                "out4CECPowerDelayTime",
            ]
            self.update_state_on_success(keys, out, val)
        else:
            logging.error("SET CEC POWER DELAY TIME FAILED")

    async def set_HDCP_support(self, inp, val):
        if inp < 1 or inp > 4 or not val.isinstance(bool):
            logging.error("Incorrect params")
            return

        success = self.client.set_HDCP_support(inp, val)
        if success:
            keys = [
                "in1HDCPSupport",
                "in2HDCPSupport",
                "in3HDCPSupport",
                "in4HDCPSupport",
            ]
            self.update_state_on_success(keys, inp, val)
        else:
            logging.error("SET HDCP SUPPORT FAILED")

    async def set_input_EDID(self, inp, edid_val):
        if inp < 1 or inp > 4:
            logging.error("Incorrect params")
            return

        success = self.client.set_input_EDID(inp, edid_val)
        if success:
            keys = ["in1EDID", "in2EDID", "in3EDID", "in4EDID"]
            self.update_state_on_success(keys, inp, edid_val)
        else:
            logging.error("SET INPUT EDID FAILED")

    async def set_mute(self, type, out, val):
        if (
            out < 1
            or out > 4
            or not val.isinstance(bool)
            or type not in ["hdmi", "spdif", "audio"]
        ):
            logging.error("Incorrect params")
            return

        success = self.client.set_mute(type, out, val)
        if success:
            keys = [
                "hdmiaudioout1",
                "hdmiaudioout2",
                "spdifaudioout1",
                "spdifaudioout2",
                "audioout1",
                "audioout2",
            ]
            # TODO update state key
            # self.update_state_on_success(keys, out, val)
        else:
            logging.error("SET MUTE FAILED")

    def update_state_on_success(self, keys, num, state):
        for key in keys:
            if str(num) in key:
                self.states[key] = state
        self._state_change_callback(self.states)

    # def async async_get_state(self):
    # return self.states
