import json

from EventManager.formatters.default_formatter import DefaultFormatter


class JsonFormatter(DefaultFormatter):
    def format(self, metadata, *args):
        data = dict(metadata)
        data.update({arg.get_key(): arg.get_value() for arg in args})
        return json.dumps(data)

    def format_message(self, metadata, message):
        data = dict(metadata)
        data["message"] = message
        return json.dumps(data)

    def format_element(self, arg):
        return json.dumps({arg.get_key(): arg.get_value()})[1:-1]

    def format_arguments(self, body, *args):
        arg_data = {arg.get_key(): arg.get_value() for arg in args}
        return f'"{body}": ' + json.dumps(arg_data)