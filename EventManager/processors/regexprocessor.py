import re

from EventManager.filehandlers.config.regex_entry import RegexEntry


class RegexProcessor:
    def __init__(self, regex_entries: list[RegexEntry] = None):
        self.regex_entries = regex_entries if regex_entries is not None else []

    def process_kv(self, event: str) -> str:
        return self._process_event(event, "KV")

    def process_json(self, event: str) -> str:
        event = re.sub(r"\s+", "", event)
        return self._process_event(event, "JSON")

    def process_xml(self, event: str) -> str:
        return self._process_event(event, "XML")

    def _process_event(self, event: str, format: str) -> str:
        for entry in self.regex_entries:
            regex = self._process_regex(format, entry.field_name, entry.regex)
            replacement = self._process_regex(format, entry.field_name, entry.replacement)
            event = re.sub(regex, replacement, event)
        return event

    def _process_regex(self, format: str, field_name: str, value: str) -> str:
        if format == "KV":
            return f'{field_name}="{value}"'
        elif format == "JSON":
            return f'"{field_name}":"{value}"'
        elif format == "XML":
            return f'<{field_name}>{value}</{field_name}>'
        else:
            return "N\\A"