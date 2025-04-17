import json
import os
import platform
import re
import time
import urllib
from datetime import datetime
from pathlib import Path

from EventManager import InternalEventManager


class LogHandler():
    __config: Config
    __current_file_name: str
    __current_internal_file_name: str
    __internal_event_manager: InternalEventManager
    __print_to_console: bool

    def __init__(self, config_path:str):
        self.__load_config_file(config_path)
        self.__set_initial_values()


    def __set_initial_values(self, config_path: str):
        """
        Load the config file and set the config attribute.
        """
        file_name: str = self.__config.get_log_file().get_file_name()
        file_extension: str = self.__config.get_log_file().get_file_extension()
        self.__current_file_name = self.__create_new_file_name(file_name, file_extension)
        file_path: str = self.__config.get_log_file().get_file_path()
        self.__config.get_log_file.set_file_path(set_correct_file_path(file_path))
        file_path: str = self.__config.get_internal_events().get_file_path()
        self.__config.get_internal_events().set_file_path(set_correct_file_path(file_path))

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
        # Get the path of the file and decode it to UTF-8 to cope with special characters
        config_path = self.set_correct_os_separator(config_path)
        path = os.path.join(os.getcwd(), config_path)
        path = urllib.parse.unquote(path, encoding='utf-8')

        # Load the config file
        try:
            with open(path, 'r', encoding='utf-8') as file:
                self.config = json.load(file)
            self.initialise_internal_event_manager()
            self.internal_event_manager.log_info("Config file loaded successfully.")
        except Exception as e:
            self.config = self.default_config()
            self.initialise_internal_event_manager()
            self.internal_event_manager.log_error(f"Could not load the config file. Using default values. Error: {str(e)}")

    def __initialise_internal_event_manager(self):
        """
        Initialise the internal event manager. If the print_to_console flag is set to true,
        the internal event manager will print to console. Otherwise, it will create a new file
        with the specified file name and file extension.
        """
        if self.__print_to_console:
            self.__config.get_event_manager().set_print_to_console(True)
            self.__internal_event_manager = InternalEventManager(self)
            return
        file_name = self.__config.get_internal_events().get_file_name()
        file_extension = self.__config.get_internal_events().get_file_extension()
        self.__current_internal_file_name = self.__create_new_file_name(file_name,file_extension)

    def __create_new_file_name(self, file_name:str, file_extension:str) -> str:
        """
        Create a new file name based on the current date and time.

        :param file_name: The base file name.
        :param file_extension: The file extension.
        :return: The new file name.
        """
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{file_name}-{current_time}.{file_extension}"

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