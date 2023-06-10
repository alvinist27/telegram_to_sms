"""Module with choices using in telegram client initialization."""

from enum import Enum


class YamlConfigKeys(str, Enum):
    """Enum for yaml config file keys."""

    tg_user_data = 'tg_user_data'


class UserDataKeys(str, Enum):
    """Enum for config client telegram credentials."""

    api_id = 'api_id'
    api_hash = 'api_hash'
    phone_number = 'phone_number'
