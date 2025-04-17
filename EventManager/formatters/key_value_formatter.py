from EventManager.formatters.default_formatter import DefaultFormatter


class KeyValueFormatter(DefaultFormatter):
    def format(self, metadata, *args):
        builder = " ".join(str(arg) for arg in args)
        return " ".join(f"{k}=\"{v}\"" for k, v in metadata.items()) + " " + builder

    def format_message(self, metadata, message):
        return " ".join(f"{k}=\"{v}\"" for k, v in metadata.items()) + f" message={message}"
