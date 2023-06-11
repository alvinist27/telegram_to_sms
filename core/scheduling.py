"""Module for scheduling functionality."""

import asyncio
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.classes import SMSController, TelegramController
from core.settings import POLL_DAYS_INTERVAL, SENDING_DELTA_HOURS

scheduler = AsyncIOScheduler()
polling_start_date = datetime.now()
sending_start_date = polling_start_date + timedelta(hours=SENDING_DELTA_HOURS)


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
