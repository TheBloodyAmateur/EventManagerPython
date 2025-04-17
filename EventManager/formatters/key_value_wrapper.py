
class KeyValueWrapper():
    """
    A class to wrap a key-value pair.
    """

    __key: str
    __value: str

    def __init__(self, key: str, value: str):
        """
        Initialize the KeyValueWrapper with a key and value.

        :param key: The key of the key-value pair.
        :param value: The value of the key-value pair.
        """
        self.__key = key
        self.__value = value

    def get_key(self):
        """
        Get the key of the KeyValueWrapper.

        :return: The key of the KeyValueWrapper.
        """
        return self.__key

    def get_value(self):
        """
        Get the value of the KeyValueWrapper.

        :return: The value of the KeyValueWrapper.
        """
        return self.__value

    def __str__(self):
        """
        Return a string representation of the KeyValueWrapper.

        :return: A string representation of the KeyValueWrapper.
        """
        return f"{self.__key}=\"{self.__value}\""