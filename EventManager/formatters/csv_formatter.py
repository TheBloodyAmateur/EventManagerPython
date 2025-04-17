from EventManager.formatters.default_formatter import DefaultFormatter


class CsvFormatter(DefaultFormatter):
    def format(self, metadata, *args):
        meta = ",".join(metadata.values())
        arg_values = ",".join(arg.get_value() for arg in args)
        return f"{meta},{arg_values}"

    def format_message(self, metadata, message):
        meta = ",".join(metadata.values())
        return f"{meta},{message}"

    def format_element(self, arg):
        return arg.get_value()

    def format_arguments(self, body, *args):
        return ",".join(arg.get_value() for arg in args)