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
        telnet_client.connect()
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
            "CECPower": False,
            "CECAutoPower": False,
            "CECPowerDelayTime": 2,
            "HDCPSupport": False,
            "input1EDID": 17,
            "input2EDID": 17,
            "input3EDID": 17,
            "input4EDID": 17,
            "mute": False,
        }

        _LOGGER.info("RESETTING HDMI SWITCH")

        self.name = "HDMI Matrix"

        self.client = telnet_client

    async def switch_input(self, inp, output):
        success = self.client.switch_input(inp, output)
        inp = int(inp)
        logging.info(f"SWITCHING INPUT {inp} {output}")
        if success:
            if (inp) == 1:
                self.states["input1"] = output
                logging.info(f"SWITCHING INPUT1 {inp} {output}")
            if (inp) == 2:
                self.states["input2"] = output
                logging.info(f"SWITCHING INPUT2 {inp} {output}")
            if (inp) == 3:
                self.states["input3"] = output
                logging.info(f"SWITCHING INPUT3 {inp} {output}")
            if (inp) == 4:
                self.states["input4"] = output
                logging.info(f"SWITCHING INPUT4 {inp} {output}")

    async def set_CEC_power(self, val):
        success = self.client.set_CEC_power(val)
        if success:
            self.states["CECPOower"] = val

    async def set_CEC_auto_power(self, val):
        success = self.client.set_CEC_auto_power(val)
        if success:
            self.states["CECAutoPower"] = val

    async def set_CEC_power_delay_time(self, val):
        success = self.client.set_CEC_power_delay_time(val)
        if success:
            self.states["CECPowerDelayTime"] = val

    async def set_HDCP_support(self, val):
        success = self.client.set_HDCP_support(val)
        if success:
            self.states["HDCPSupport"] = val

    async def set_input_EDID(self, inp, edid_val):
        success = self.client.set_input_EDID(inp, edid_val)
        if success:
            if (inp) == 1:
                self.states["input1EDID"] = edid_val
            if (inp) == 2:
                self.states["input1EDID"] = edid_val
            if (inp) == 3:
                self.states["input1EDID"] = edid_val
            if (inp) == 4:
                self.states["input1EDID"] = edid_val

    async def set_mute(self, val):
        success = self.client.set_mute(val)
        if success:
            self.states["mute"] = val
