from EventManager.formatters.default_formatter import DefaultFormatter


class XmlFormatter(DefaultFormatter):
    def format(self, metadata, *args):
        builder = self._xml_metadata(metadata)
        for arg in args:
            builder += f"<{arg.get_key()}>{arg.get_value()}</{arg.get_key()}>"
        return builder + "</event>"

    def format_message(self, metadata, message):
        builder = self._xml_metadata(metadata)
        return builder + f"<message>{message}</message></event>"

    def format_element(self, arg):
        return f"<{arg.get_key()}>{arg.get_value()}</{arg.get_key()}>"

    def format_arguments(self, body, *args):
        builder = f"<{body}>"
        for arg in args:
            builder += f"<{arg.get_key()}>{arg.get_value()}</{arg.get_key()}>"
        return builder + f"</{body}>"

    def _xml_metadata(self, metadata):
        return "<event>" + "".join(f"<{k}>{v}</{k}>" for k, v in metadata.items())