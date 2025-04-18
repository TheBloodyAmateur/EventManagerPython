import os

from EventManager.outputs.Output import Output


class LogOutput(Output):
    def write(self, log_handler, event):
        try:
            if not log_handler.check_if_internal_log_file_exists():
                log_handler.create_internal_log_file()
            file_path = log_handler.config().internal_events().get_file_path()
            with open(os.path.join(file_path, log_handler.get_current_internal_file_name()), "a") as file:
                file.write(event + "\n")
        except Exception as e:
            print(f"An error occurred in write_event_to_log_file: {e}")

    def write(self, internal_event_manager, event):
        try:
            log_handler = internal_event_manager.get_log_handler()
            if not log_handler.check_if_log_file_exists():
                log_handler.create_log_file()
            file_path = log_handler.config().log_file().get_file_path()
            with open(os.path.join(file_path, log_handler.get_current_file_name()), "a") as file:
                file.write(event + "\n")
        except Exception as e:
            internal_event_manager.log_error(f"An error occurred in write_event_to_log_file: {e}")