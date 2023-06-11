"""Module for scheduling functionality."""

import asyncio
import os
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.classes import SMSController, TelegramController
from core.settings import POLL_DAYS_INTERVAL, SENDING_DELTA_HOURS, TG_MESSAGES_DIR

scheduler = AsyncIOScheduler()
polling_start_date = datetime.now()
sending_start_date = polling_start_date + timedelta(hours=SENDING_DELTA_HOURS)
cleaning_start_date = sending_start_date + timedelta(hours=SENDING_DELTA_HOURS)


@scheduler.scheduled_job(trigger='interval', days=POLL_DAYS_INTERVAL, start_date=polling_start_date)
async def poll_messages() -> None:
    """Poll and save unread messages from Telegram."""
    tg_controller = TelegramController()
    await tg_controller.save_unread_messages()


@scheduler.scheduled_job(trigger='interval', days=POLL_DAYS_INTERVAL, start_date=sending_start_date)
def send_messages() -> None:
    """Send Telegram messages via SMS."""
    sms_controller = SMSController()
    sms_controller.send_messages()


@scheduler.scheduled_job(trigger='interval', days=POLL_DAYS_INTERVAL, start_date=cleaning_start_date)
def clean_messages() -> None:
    """Clean tg messages dir."""
    for filename in os.listdir(TG_MESSAGES_DIR):
        file_path = os.path.join(TG_MESSAGES_DIR, filename)
        os.remove(file_path)


async def main():
    scheduler.start()
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
