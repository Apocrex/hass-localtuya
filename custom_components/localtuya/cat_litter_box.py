"""Platform to locally control Tuya-based automated cat litter boxes"""

import logging
from functools import partial
from .config_flow import col_to_select

import voluptuous as vol
from homeassistant.components.lawn_mower import (
    DOMAIN,
    LawnMowerActivity,
    LawnMowerEntity,
    LawnMowerEntityFeature,
)

from .entity import LocalTuyaEntity, async_setup_entry
from .const import CONF_FAULT_DP

_LOGGER = logging.getLogger(__name__)


def flow_schema(dps):
    """Return schema used in config flow."""
    return {
        vol.Optional(CONF_FAULT_DP): col_to_select(dps, is_dps=True),
    }


class LocalTuyaCatLitterBox(LocalTuyaEntity, LawnMowerEntity):
    """Tuya cat litter box device."""

    def __init__(self, device, config_entry, switchid, **kwargs):
        """Initialize a new LocalTuyaCatLitterBox."""
        super().__init__(device, config_entry, switchid, _LOGGER, **kwargs)
        self._activity = LawnMowerActivity.DOCKED

    @property
    def supported_features(self) -> LawnMowerEntityFeature:
        """Flag supported features."""
        return LawnMowerEntityFeature.START_MOWING | LawnMowerEntityFeature.DOCK

    @property
    def activity(self) -> LawnMowerActivity:
        """Return the current activity."""
        return self._activity

    async def async_start_mowing(self) -> None:
        """Start a cleaning cycle."""
        await self._device.set_dp(True, self._dp_id)

    async def async_dock(self) -> None:
        """Stop cleaning and return to idle."""
        await self._device.set_dp(False, self._dp_id)

    def status_updated(self):
        """Device status was updated."""
        if self.has_config(CONF_FAULT_DP) and self.dp_value(CONF_FAULT_DP):
            self._activity = LawnMowerActivity.ERROR
            return

        if self.dp_value(self._dp_id):
            self._activity = LawnMowerActivity.MOWING
        else:
            self._activity = LawnMowerActivity.DOCKED


async_setup_entry = partial(async_setup_entry, DOMAIN, LocalTuyaCatLitterBox, flow_schema)
