"""Module with defining classes."""

import asyncio
import logging
import os
from datetime import datetime
from textwrap import wrap
from typing import Any, Optional

import yaml
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from core.choices import SMSApiDataKeys, TgUserDataKeys, YamlConfigKeys
from core.settings import (
    CLIENT_SESSION_FILE_NAME, CLIENT_SYSTEM_VERSION, CONFIG_FILE_PATH, SMS_SYMBOLS_COUNT_LIMIT, TG_MESSAGES_DIR,
)

logger = logging.getLogger('core.classes')


class BaseAdapter(object):
    """Base adapter class."""

    def write(self, content: Any) -> Any:
        """Write data to destination.

        Args:
            content: data to be written.
        """
        pass

    def read(self) -> Any:
        """Read data from a data source."""
        pass


class FileAdapter(BaseAdapter):
    """Adapter class for i/o file operations."""

    def __init__(self, file_path: str) -> None:
        """Initialize FileAdapter object.

        Args:
            file_path: path to file for write and read operations.
        """
        self.file_path = file_path

    def write(self, content: str) -> None:
        """Write data to a file.

        Args:
            content: data to be written to the file.
        """
        try:
            with open(self.file_path, 'w') as file_obj:
                file_obj.write(content)
        except FileNotFoundError as file_error:
            error_message = f'FileNotFoundError. Create folders first. Error: {file_error}'
        else:
            return None
        logger.error(error_message)
        return None

    def read(self) -> Optional[str]:
        """Read data from a file.

        Returns:
            Reading file content.
        """
        try:
            with open(self.file_path, 'r') as file_obj:
                file_content = file_obj.read()
        except FileNotFoundError as file_error:
            error_message = f'FileNotFoundError. File with specified path not exists. Error: {file_error}'
        else:
            return file_content
        logger.error(error_message)
        return None


class YamlFileAdapter(BaseAdapter):
    """Adapter class for i/o yaml file operations."""

    def __init__(self, file_path: str) -> None:
        """Initialize YamlFileAdapter object.

        Args:
            file_path: path to yaml file for write and read operations.
        """
        self.file_path = file_path

    def write(self, content: bytes) -> None:
        """Write data to a yaml file.

        Args:
            content: data to be written to the yaml file.
        """
        try:
            with open(self.file_path, 'wb') as file_obj:
                yaml.safe_dump(content, file_obj)
        except FileNotFoundError as file_error:
            error_message = f'FileNotFoundError. Create folders first. Error: {file_error}'
        except yaml.YAMLError as yaml_error:
            error_message = f'YAMLError. YAML parser encounters an error condition. Error: {yaml_error}'
        else:
            return None
        logger.error(error_message)
        return None

    def read(self) -> Optional[dict]:
        """Read data from a yaml file.

        Returns:
            Reading yaml file content.
        """
        try:
            with open(self.file_path, 'r') as file_obj:
                file_content = yaml.safe_load(file_obj)
        except FileNotFoundError as file_error:
            error_message = f'FileNotFoundError. File with specified path not exists. Error: {file_error}'
        except yaml.YAMLError as yaml_error:
            error_message = f'YAMLError. YAML parser encounters an error condition. Error: {yaml_error}'
        else:
            return file_content
        logger.error(error_message)
        return None


class TelegramController(object):
    """Controller class for interacting with Telegram messages."""

    def __init__(self) -> None:
        """Initialize TelegramController object."""
        config_settings = YamlFileAdapter(CONFIG_FILE_PATH).read()
        user_auth_data = config_settings[YamlConfigKeys.tg_user_data]
        self.api_id, self.api_hash = user_auth_data[TgUserDataKeys.api_id], user_auth_data[TgUserDataKeys.api_hash]
        self.phone_number = user_auth_data[TgUserDataKeys.phone_number]

    async def _auth_client(self, client: TelegramClient) -> None:
        """Authorize Telegram client.

        Args:
            client: TelegramClient instance.
        """
        if not await client.is_user_authorized():
            await client.send_code_request(self.phone_number)
            try:
                await client.sign_in(self.phone_number, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Enter password: '))

    @staticmethod
    async def _save_unread_messages(client: TelegramClient) -> None:
        """Save unread Telegram messages to specified dir.

        Args:
            client: TelegramClient instance.
        """
        async for dialog in client.iter_dialogs():
            if not dialog.unread_count:
                continue
            messages = await client.get_messages(dialog.entity, limit=dialog.unread_count)
            title = getattr(dialog.entity, 'title', 'default')
            result_messages = []
            for message in reversed(messages):
                result_messages.append(message.text)
                await client.send_read_acknowledge(dialog.entity, max_id=message.id)
            channel_content_path = os.path.join(TG_MESSAGES_DIR, f'{title}_{datetime.now().date()}')
            channel_content = '\n'.join(result_messages)
            FileAdapter(channel_content_path).write(channel_content)

    async def save_unread_messages(self) -> None:
        """Connect to Telegram and save unread messages."""
        async with TelegramClient(
            session=CLIENT_SESSION_FILE_NAME,
            api_id=self.api_id,
            api_hash=self.api_hash,
            system_version=CLIENT_SYSTEM_VERSION,
        ) as client:
            await client.connect()
            await self._auth_client(client)
            await self._save_unread_messages(client)


class SMSController(object):
    """Controller class for interacting with SMSC API."""

    def __init__(self):
        """Initialize SMSController object."""
        from core.smsc_api import SMSC
        config_settings = YamlFileAdapter(CONFIG_FILE_PATH).read()
        self.receiver_phone = config_settings[YamlConfigKeys.smsc_api_data][SMSApiDataKeys.receiver_phone_number]
        self.smsc_client = SMSC()

    def _send_message(self, message_text: str) -> None:
        """Send message using the SMSC client.

        Args:
            message_text: The text message to be sent.
        """
        wrapped_messages = wrap(message_text, width=SMS_SYMBOLS_COUNT_LIMIT)
        for message in wrapped_messages:
            self.smsc_client.send_sms(str(self.receiver_phone).encode(), message.encode(), translit=1)

    def send_messages(self) -> None:
        """Send SMS messages for each file in the TG_MESSAGES_DIR directory."""
        for filename in os.listdir(TG_MESSAGES_DIR):
            file_path = os.path.join(TG_MESSAGES_DIR, filename)
            file_content = FileAdapter(file_path=file_path).read()
            self._send_message(file_content)


if __name__ == '__main__':
    telegram_controller = TelegramController()
    asyncio.run(telegram_controller.save_unread_messages())
