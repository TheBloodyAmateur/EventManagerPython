from abc import ABC, abstractmethod


class Compressors():
    @staticmethod
    @abstractmethod
    def compress(file_path: str) -> None:
        """
        Compress the given file.

        :param file_path: Path to the file to be compressed.
        """
        pass
        pass

    @staticmethod
    def set_new_file_extension(file_path: str, compression_type: str) -> str:
        """
        Sets a new file extension based on the compression type.

        :param file_path: The original file path.
        :param compression_type: The type of compression (e.g., "gzip", "zip").
        :return: The new file path with the updated extension.
        """
        return f"{file_path.rsplit('.', 1)[0]}.{compression_type}"