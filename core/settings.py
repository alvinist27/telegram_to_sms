"""Settings for telegram_to_sms project."""

import os
from pathlib import Path

POLL_DAYS_INTERVAL = 3

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'config.yaml')
CLIENT_SESSION_FILE_NAME = 'session'
CLIENT_SYSTEM_VERSION = '4.16.30-vxCUSTOM'
