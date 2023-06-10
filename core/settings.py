"""Settings for telegram_to_sms project."""

import os
from pathlib import Path

POLL_DAYS_INTERVAL = 3

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'config.yaml')
SESSION_FILE_NAME = 'session'
