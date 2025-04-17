import gzip

from EventManager.compressors.compressors import Compressors


class GzipCompressor(Compressors):
    @staticmethod
    def compress(file_path: str):
        try:
            output_path = Compressors.set_new_file_extension(file_path, 'gz')
            with open(file_path, 'rb') as file_input, \
                    open(output_path, 'wb') as file_output, \
                    gzip.GzipFile(fileobj=file_output, mode='wb') as gzip_output:

                while chunk := file_input.read(1024):
                    gzip_output.write(chunk)
        except Exception as e:
            print(f"Error compressing file to GZIP: {e}")