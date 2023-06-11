"""Module with choices using in telegram client initialization."""

from enum import Enum


class YamlConfigKeys(str, Enum):
    """Enum for yaml config file keys."""

    tg_user_data = 'tg_user_data'
    smsc_api_data = 'smsc_api_data'


class TgUserDataKeys(str, Enum):
    """Enum for config client telegram credentials."""

    api_id = 'api_id'
    api_hash = 'api_hash'
    phone_number = 'phone_number'


class SMSApiDataKeys(str, Enum):
    """Enum for config client SMSC Api credentials."""

    login = 'login'
    password = 'password'
    receiver_phone_number = 'receiver_phone_number'
