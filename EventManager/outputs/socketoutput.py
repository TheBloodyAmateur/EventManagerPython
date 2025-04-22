import socket
from typing import TYPE_CHECKING

from EventManager.outputs import Batch
from EventManager.outputs.Output import Output

if TYPE_CHECKING:
    from EventManager.internal_event_manager import InternalEventManager
    from EventManager.filehandlers.log_handler import LogHandler


class SocketOutput(Output):

    __socket_settings: list
    __batch: Batch = None

    def __init__(self, socket_settings: list):
        """
        Constructor for the SocketOutput class.
        :param socket_settings: The settings for the socket output.
        """
        self.__socket_settings = socket_settings
        self.__batch = Batch(max_size=65536)

    def write(self, loghandler: "LogHandler", event: str):
        if not self.__batch.try_add(event=event):
            self.send_to_socket("\n".join(self.__batch.get_batch()))
            self.__batch.clear_batch()
            self.__batch.try_add(event)

    def write(self, internal_event_manager: "InternalEventManager", event: str):
        if not self.__batch.try_add(event=event):
            bytes_size = self.__batch.get_current_size_in_bytes()
            size = len(self.__batch.get_batch())
            internal_event_manager.log_info(f"Sending {size} events to socket. Total size: {bytes_size} bytes.")
            self.send_to_socket_with_manager(internal_event_manager, "\n".join(self.__batch.get_batch()))
            self.__batch.clear_batch()
            self.__batch.try_add(event=event)

    def send_to_socket(self, event):
        for socket_entry in self.__socket_settings:
            try:
                with socket.create_connection((socket_entry['host'], socket_entry['port'])) as sock:
                    sock.sendall(event.encode('utf-8'))
            except Exception as e:
                print(f"An error occurred in send_to_socket: {e}")

    def send_to_socket_with_manager(self, internal_event_manager, event):
        for socket_entry in self.__socket_settings:
            try:
                with socket.create_connection((socket_entry.host, socket_entry.port)) as sock:
                    sock.sendall(event.encode('utf-8'))
            except Exception as e:
                internal_event_manager.log_error(f"An error occurred in send_to_socket: {e}")