from .const import DOMAIN
from . import HDMIMatrix
from homeassistant.helpers.entity import Entity


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    hdmi_matrix = hass.data[DOMAIN]
    entity = HDMIMatrixEntity(hdmi_matrix)
    async_add_entities([entity])


class HDMIMatrixEntity(Entity):
    def __init__(self, device: HDMIMatrix):
        self._device = device
        device.add_state_change_callback(self.handle_state_change)

    def handle_state_change(self, new_state):
        # Update internal state
        self._state = new_state
        # Schedule an update in HA
        self.async_schedule_update_ha_state()

    @property
    def name(self):
        return self._device.name

    @property
    def state(self):
        return self._device.states["input1"]
        # Return the primary state of the entity
        # Example: return self._device.states['input1']

    @property
    def extra_state_attributes(self):
        # Return additional states as attributes
        return self._device.states

    @property
    def unique_id(self):
        return "hdmi_matrix"

    #async def async_update(self):
    #    self._state = await self._device.async_get_state()
