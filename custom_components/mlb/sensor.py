import logging
import uuid

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify
from . import AlertsDataUpdateCoordinator

from .const import (
    ATTRIBUTION,
    CONF_TIMEOUT,
    CONF_TEAM_ID,
    COORDINATOR,
    DEFAULT_ICON,
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_TEAM_ID): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Configuration from yaml"""
    if DOMAIN not in hass.data.keys():
        hass.data.setdefault(DOMAIN, {})
        config.entry_id = slugify(f"{config.get(CONF_TEAM_ID)}")
        config.data = config
    else:
        config.entry_id = slugify(f"{config.get(CONF_TEAM_ID)}")
        config.data = config

    # Setup the data coordinator
    coordinator = AlertsDataUpdateCoordinator(
        hass,
        config,
        config[CONF_TIMEOUT],
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    hass.data[DOMAIN][config.entry_id] = {
        COORDINATOR: coordinator,
    }
    async_add_entities([MLBScoresSensor(hass, config)], True)


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup the sensor platform."""
    async_add_entities([MLBScoresSensor(hass, entry)], True)


class MLBScoresSensor(CoordinatorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(hass.data[DOMAIN][entry.entry_id][COORDINATOR])
        self._config = entry
        self._name = entry.data[CONF_NAME]
        self._icon = DEFAULT_ICON
        self._state = "PRE"
        self._date = None
        self._first_pitch = None
        self.inning = None
        self._clock = None
        self._venue = None
        self._location = None
        self._tv_network = None
        self._team_abbr = None
        self._team_id = None
        self._team_name = None
        self._team_record = None
        self._team_homeaway = None
        self._team_logo = None
        self._team_colors = None
        self._team_score = None
        self._team_inning_1 = None
        self._team_inning_2 = None
        self._team_inning_3 = None
        self._team_inning_4 = None
        self._team_inning_5 = None
        self._team_inning_6 = None
        self._team_inning_7 = None
        self._team_inning_8 = None
        self._team_inning_9 = None
        self._opponent_abbr = None
        self._opponent_id = None
        self._opponent_name = None
        self._opponent_record = None
        self._opponent_homeaway = None
        self._opponent_logo = None
        self._opponent_colors = None
        self._opponent_score = None
        self._opponent_inning_1 = None
        self._opponent_inning_2 = None
        self._opponent_inning_3 = None
        self._opponent_inning_4 = None
        self._opponent_inning_5 = None
        self._opponent_inning_6 = None
        self._opponent_inning_7 = None
        self._opponent_inning_8 = None
        self._opponent_inning_9 = None
        self._last_update = None
        self._last_play = None
        self._team_id = entry.data[CONF_TEAM_ID]
        self.coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]

    @property
    def unique_id(self):
        """
        Return a unique, Home Assistant friendly identifier for this entity.
        """
        return f"{slugify(self._name)}_{self._config.entry_id}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        elif "state" in self.coordinator.data.keys():
            return self.coordinator.data["state"]
        else:
            return None

    @property
    def extra_state_attributes(self):
        """Return the state message."""
        attrs = {}

        if self.coordinator.data is None:
            return attrs

        attrs[ATTR_ATTRIBUTION] = ATTRIBUTION
        attrs["date"] = self.coordinator.data["date"]
        attrs["first_pitch"] = self.coordinator.data["first_pitch"]
        attrs["inning"] = self.coordinator.data["inning"]
        attrs["venue"] = self.coordinator.data["venue"]
        attrs["location"] = self.coordinator.data["location"]
        attrs["tv_network"] = self.coordinator.data["tv_network"]
        attrs["team_abbr"] = self.coordinator.data["team_abbr"]
        attrs["team_id"] = self.coordinator.data["team_id"]
        attrs["team_name"] = self.coordinator.data["team_name"]
        attrs["team_record"] = self.coordinator.data["team_record"]
        attrs["team_homeaway"] = self.coordinator.data["team_homeaway"]
        attrs["team_logo"] = self.coordinator.data["team_logo"]
        attrs["team_colors"] = self.coordinator.data["team_colors"]
        attrs["team_score"] = self.coordinator.data["team_score"]
        attrs["team_inning_1"] = self.coordinator.data["team_inning_1"]
        attrs["team_inning_2"] = self.coordinator.data["team_inning_2"]
        attrs["team_inning_3"] = self.coordinator.data["team_inning_3"]
        attrs["team_inning_4"] = self.coordinator.data["team_inning_4"]
        attrs["team_inning_5"] = self.coordinator.data["team_inning_5"]
        attrs["team_inning_6"] = self.coordinator.data["team_inning_6"]
        attrs["team_inning_7"] = self.coordinator.data["team_inning_7"]
        attrs["team_inning_8"] = self.coordinator.data["team_inning_8"]
        attrs["team_inning_9"] = self.coordinator.data["team_inning_9"]
        attrs["opponent_abbr"] = self.coordinator.data["opponent_abbr"]
        attrs["opponent_id"] = self.coordinator.data["opponent_id"]
        attrs["opponent_name"] = self.coordinator.data["opponent_name"]
        attrs["opponent_record"] = self.coordinator.data["opponent_record"]
        attrs["opponent_homeaway"] = self.coordinator.data["opponent_homeaway"]
        attrs["opponent_logo"] = self.coordinator.data["opponent_logo"]
        attrs["opponent_colors"] = self.coordinator.data["opponent_colors"]
        attrs["opponent_score"] = self.coordinator.data["opponent_score"]
        attrs["opponent_inning_1"] = self.coordinator.data["opponent_inning_1"]
        attrs["opponent_inning_2"] = self.coordinator.data["opponent_inning_2"]
        attrs["opponent_inning_3"] = self.coordinator.data["opponent_inning_3"]
        attrs["opponent_inning_4"] = self.coordinator.data["opponent_inning_4"]
        attrs["opponent_inning_5"] = self.coordinator.data["opponent_inning_5"]
        attrs["opponent_inning_6"] = self.coordinator.data["opponent_inning_6"]
        attrs["opponent_inning_7"] = self.coordinator.data["opponent_inning_7"]
        attrs["opponent_inning_8"] = self.coordinator.data["opponent_inning_8"]
        attrs["opponent_inning_9"] = self.coordinator.data["opponent_inning_9"]
        attrs["last_update"] = self.coordinator.data["last_update"]
        attrs["last_play"] = self.coordinator.data["last_play"]

        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success