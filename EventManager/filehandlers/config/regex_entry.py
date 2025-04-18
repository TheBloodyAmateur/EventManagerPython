

class RegexEntry():
    field_name: str
    regex: str
    replacement: str

    def __init__(self, field_name: str, regex: str, replacement: str):
        """
        Constructor for the RegexEntry class.
        :param field_name: The name of the field to be modified.
        :param regex: The regular expression to match.
        :param replacement: The replacement string.
        """
        self.field_name = field_name
        self.regex = regex
        self.replacement = replacement

    @property
    def field_name(self):
        return self.__field_name

    @field_name.setter
    def field_name(self, value: str):
        self.__field_name = value

    @property
    def regex(self):
        return self.__regex

    @regex.setter
    def regex(self, value: str):
        self.__regex = value

    @property
    def replacement(self):
        return self.__replacement

    @replacement.setter
    def replacement(self, value: str):
        self.__replacement = value