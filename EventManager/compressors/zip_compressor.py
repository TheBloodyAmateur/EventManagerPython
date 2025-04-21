import zipfile
from pathlib import Path

from EventManager.compressors.compressors import Compressors


class ZipCompressor(Compressors):
    """
    A class for compressing files using the ZIP format.
    """
    @staticmethod
    def compress(file_path: str):
        try:
            output_path = Compressors.set_new_file_extension(file_path, 'zip')
            with open(file_path, 'rb') as file_input, \
                 open(output_path, 'wb') as file_output, \
                 zipfile.ZipFile(file_output, 'w', zipfile.ZIP_DEFLATED) as zip_output:

                zip_output.writestr(Path(file_path).name, file_input.read())
        except Exception as e:
            print(f"Error compressing file to ZIP: {e}")