"""Settings for telegram_to_sms project."""

import os
from pathlib import Path

POLL_DAYS_INTERVAL = 3
SENDING_DELTA_HOURS = 6

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'config.yaml')
TG_MESSAGES_DIR = os.path.join(BASE_DIR, 'telegram_messages')
os.makedirs(TG_MESSAGES_DIR, exist_ok=True)

CLIENT_SESSION_FILE_NAME = 'session'
CLIENT_SYSTEM_VERSION = '4.16.30-vxCUSTOM'
SMS_SYMBOLS_COUNT_LIMIT = 150
MESSAGE_DELIVERY_TIME = 20
