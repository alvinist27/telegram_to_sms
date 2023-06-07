"""Module for scheduling functionality."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.settings import POLL_DAYS_INTERVAL

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(trigger='interval', days=POLL_DAYS_INTERVAL)
def poll_messages() -> None:
    pass


if __name__ == '__main__':
    scheduler.start()
