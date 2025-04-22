import json
import os
import platform
import re
import time
from datetime import datetime
from pathlib import Path

import urllib3.util
from typing import TYPE_CHECKING

from EventManager.filehandlers.config.config import Config

class LogHandler():
    """
    The LogHandler class is responsible for managing the logging configuration and log files.
    """
    __config: Config
    __current_file_name: str
    __current_internal_file_name: str
    __internal_event_manager = None

    def __init__(self, config_path:str):
        self.__load_config_file(config_path)
        self.__set_initial_values()

    @property
    def config(self) -> Config:
        return self.__config

    @property
    def current_file_name(self) -> str:
        return self.__current_file_name

    @current_file_name.setter
    def current_file_name(self, file_name: str):
        self.__current_file_name = file_name

    @property
    def current_internal_file_name(self) -> str:
        return self.__current_internal_file_name

    @current_internal_file_name.setter
    def current_internal_file_name(self, file_name: str):
        self.__current_internal_file_name = file_name

    @property
    def internal_event_manager(self):
        return self.__internal_event_manager

    def __set_initial_values(self):
        """
        Load the config file and set the config attribute.
        """
        file_name: str = self.__config.log_file.file_name
        file_extension: str = self.__config.log_file.file_extension
        self.__current_file_name = self.__create_new_file_name(file_name, file_extension)

        file_path: str = self.__config.log_file.file_path
        self.__config.log_file.file_path = self.__set_correct_file_path(file_path)

        file_path: str = self.__config.internal_events.file_path
        self.__config.internal_events.file_path = self.__set_correct_file_path(file_path)

    @staticmethod
    def __set_correct_file_path(file_path: str) -> str:
        """
        Sets the correct file path. If the file path does not exist, the default file path is
        used based on the operating system.

        Args:
            file_path: The file path to check.

        Returns:
            The correct file path based on the operating system.
        """
        if os.path.exists(file_path):
            return file_path
        else:
            if 'windows' in platform.system().lower():
                return 'C:\\Windows\\Temp\\'
            else:
                return '/tmp/'

    def __load_config_file(self, config_path):
        """
        Loads the configuration file from the specified path.
        If the file cannot be loaded, default configuration values are used.

        :param config_path: the path to the configuration file.
        """
        from EventManager.event_manager import EventManager

        # Get the path of the file and decode it to UTF-8 to cope with special characters
        config_path = EventManager.set_correct_os_seperator(config_path)
        path = os.path.join(os.getcwd(), config_path)
        # Decode the path to UTF-8
        path = str(urllib3.util.parse_url(path))

        # Load the config file
        try:
            with open(path, 'r', encoding='utf-8') as file:
                self.__config = json.load(file)
            self.__initialise_internal_event_manager()
            self.__internal_event_manager.log_info("Config file loaded successfully.")
        except (FileNotFoundError, IsADirectoryError)  as e:
            self.__config = Config()
            self.__initialise_internal_event_manager()
            self.__internal_event_manager.log_error(f"Could not load the config file. Using default values. Error: {str(e)}")

    def __initialise_internal_event_manager(self):
        """
        Initialise the internal event manager. If the print_to_console flag is set to true,
        the internal event manager will print to console. Otherwise, it will create a new file
        with the specified file name and file extension.
        """
        from EventManager.internal_event_manager import InternalEventManager

        file_name = self.__config.internal_events.file_name
        file_extension = self.__config.internal_events.file_extension
        self.__current_internal_file_name = self.__create_new_file_name(file_name,file_extension)
        self.__internal_event_manager = InternalEventManager(self)

    def __create_new_file_name(self, file_name:str, file_extension:str) -> str:
        """
        Create a new file name based on the current date and time.

        :param file_name: The base file name.
        :param file_extension: The file extension.
        :return: The new file name.
        """
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{file_name}-{current_time+file_extension}"

    def check_if_log_file_needs_rotation(self):
        log_file_path = self.config['log_file']['file_path']
        file_name = self.config['log_file']['file_name']
        file_extension = self.config['log_file']['file_extension']
        rotation_period = self.config['log_rotate_config']['rotation_period_in_seconds']
        max_size_kb = self.config['log_rotate_config']['max_size_in_kb']

        directory = Path(log_file_path)
        if not directory.exists():
            return

        pattern = re.compile(f"{file_name}-(?P<file_timestamp>[0-9\\-]+){file_extension}$")

        for file in directory.iterdir():
            if file.is_file():
                match = pattern.match(file.name)
                if match:
                    creation_time = file.stat().st_ctime
                    current_time = time.time()
                    file_size_kb = file.stat().st_size / 1024

                    if (current_time - creation_time) > rotation_period:
                        self.rotate_log_file(file)
                        self.current_file_name = self.__create_new_file_name(file_name, file_extension)
                    elif file_size_kb > max_size_kb:
                        self.rotate_log_file(file)
                        self.current_file_name = self.__create_new_file_name(file_name, file_extension)

    def rotate_log_file(self, file: Path):
        """
        Rotate the log file by renaming it with a timestamp.

        :param file: The log file to rotate.
        """
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_file_name = f"{file.stem}-{current_time}{file.suffix}"
        new_file_path = file.parent / new_file_name
        os.rename(file, new_file_path)

    def check_if_log_file_exists(self):
        """
        Check if the log file exists.

        :return: True if the log file exists, False otherwise.
        """
        log_file_path = self.config.log_file.file_path
        file_name = self.current_file_name

        log_file = os.path.join(log_file_path, f"{file_name}")
        return os.path.exists(log_file)

    def check_if_internal_log_file_exists(self) -> bool:
        """
        Check if the internal log file exists.

        :return: True if the internal log file exists, False otherwise.
        """
        internal_log_file_path = self.config.internal_events.file_path
        file_name = self.config.internal_events.file_name
        file_extension = self.config.internal_events.file_extension

        internal_log_file = os.path.join(internal_log_file_path, f"{file_name}{file_extension}")
        return os.path.exists(internal_log_file)

    def create_log_file(self):
        """
        Creates a new log file with the specified file name and file extension.
        """
        log_file_path = self.config.log_file.file_path
        file_name = self.current_file_name

        log_file = os.path.join(log_file_path, f"{file_name}")

        with open(log_file, 'w', encoding='utf-8'):
            pass

    def create_internal_log_file(self):
        """
        Creates a new internal log file with the specified file name and file extension.
        """
        internal_log_file_path = self.config.internal_events.file_path
        file_name = self.__current_internal_file_name

        internal_log_file = os.path.join(internal_log_file_path, f"{file_name}")

        with open(internal_log_file, 'w', encoding='utf-8'):
            pass