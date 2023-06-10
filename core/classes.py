"""Module with defining  classes."""

import asyncio
import logging
from typing import Any, Optional

import yaml
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from core.choices import UserDataKeys, YamlConfigKeys
from core.settings import CLIENT_SESSION_FILE_NAME, CLIENT_SYSTEM_VERSION, CONFIG_FILE_PATH

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


class YamlFileAdapter(BaseAdapter):
    """Adapter class for i/o yaml file operations."""

    def __init__(self, file_path: str) -> None:
        """Initialize YamlFileAdapter object.

        Args:
            file_path: path to yaml file for write and read operations.
        """
        self.file_path = file_path

    def write(self, content: bytes) -> None:
        """Write data to a file.

        Args:
            content: data to be written to the file.
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


class TelegramController(object):
    def __init__(self):
        config_settings = YamlFileAdapter(CONFIG_FILE_PATH).read()
        user_auth_data = config_settings[YamlConfigKeys.tg_user_data]
        self.api_id, self.api_hash = user_auth_data[UserDataKeys.api_id], user_auth_data[UserDataKeys.api_hash]
        self.phone_number = user_auth_data[UserDataKeys.phone_number]

    async def get_unread_messages(self):
        async with TelegramClient(
            session=CLIENT_SESSION_FILE_NAME,
            api_id=self.api_id,
            api_hash=self.api_hash,
            system_version=CLIENT_SYSTEM_VERSION,
        ) as client:
            await client.connect()
            if not await client.is_user_authorized():
                await client.send_code_request(self.phone_number)
                try:
                    await client.sign_in(self.phone_number, input('Enter the code: '))
                except SessionPasswordNeededError:
                    await client.sign_in(password=input('Password: '))

            async for dialog in client.iter_dialogs():
                if not dialog.unread_count:
                    continue
                messages = await client.get_messages(dialog.entity, limit=dialog.unread_count)
                title = getattr(dialog.entity, 'title', 'default')
                for message in reversed(messages):
                    print(title)
                    print(message.text)
                    await client.send_read_acknowledge(dialog.entity, max_id=message.id)


if __name__ == '__main__':
    telegram_controller = TelegramController()
    asyncio.run(telegram_controller.get_unread_messages())
