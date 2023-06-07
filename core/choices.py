"""Module with choices using in telegram client initialization."""

from enum import Enum


class YamlConfigKeys(Enum):
    """Enum for yaml config file keys."""

    tg_user_data = 'tg_user_data'
    channel_ids = 'channel_ids'


class UserDataKeys(Enum):
    """Enum for config client telegram credentials."""

    api_id = 'api_id'
    api_hash = 'api_hash'
