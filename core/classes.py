"""Module with defining  classes."""

import logging
from typing import Any, Optional

import yaml

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

    def read(self) -> Optional[str]:
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
    pass
