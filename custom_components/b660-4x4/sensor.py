from .const import DOMAIN
from .. import HDMIMatrix
from homeassistant.helpers.entity import Entity


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    hdmi_matrix = hass.data[DOMAIN]
    entity = HDMIMatrixEntity(hdmi_matrix)
    async_add_entities([entity])


class HDMIMatrixEntity(Entity):
    def __init__(self, device: HDMIMatrix):
        self._device = device

    @property
    def name(self):
        return self._device.name

    @property
    def state(self):
        return self._device.states["CECPower"]
        # Return the primary state of the entity
        # Example: return self._device.states['input1']

    @property
    def extra_state_attributes(self):
        # Return additional states as attributes
        return self._device.states

    @property
    def unique_id(self):
        return "hdmi_matrix"

    # Implement any actions as methods or service callbacks
    # For example, switching inputs, changing settings, etc
