from EventManager.formatters.formatter_strategy import FormatterStrategy


class DefaultFormatter(FormatterStrategy):
    def format(self, metadata, *args):
        builder = " ".join(str(arg) for arg in args)
        return f"[{metadata['time']}] {metadata['level']} {metadata['className']} {metadata['methodName']} {metadata['lineNumber']}: {builder}"

    def format_message(self, metadata, message):
        return f"[{metadata['time']}] {metadata['level']} {metadata['className']} {metadata['methodName']} {metadata['lineNumber']}: {message}"

    def format_element(self, arg):
        return str(arg)

    def format_arguments(self, body, *args):
        return " ".join(str(arg) for arg in args)