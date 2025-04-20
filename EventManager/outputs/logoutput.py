import os

from EventManager.outputs.Output import Output


class LogOutput(Output):
    """
    A class to handle log output for events.
    """
    def write(self, target, event: str):
        try:
            if hasattr(target, 'log_handler'):  # It's an internal_event_manager
                log_error = target.log_error
                log_handler = target.log_handler
                if not log_handler.check_if_log_file_exists():
                    log_handler.create_log_file()
                file_path = log_handler.config.log_file.file_path
                file_name = log_handler.current_file_name
            else:  # It's a plain log_handler
                log_error = print  # Fallback logger
                log_handler = target
                if not log_handler.check_if_internal_log_file_exists():
                    log_handler.create_internal_log_file()
                file_path = log_handler.config.internal_events.file_path
                file_name = log_handler.current_internal_file_name
            with open(os.path.join(file_path, file_name), "a", encoding="UTF-8") as file:
                file.write(event + "\n")
        except Exception as e:
            log_error(f"An error occurred in write_event_to_log_file: {e}")
