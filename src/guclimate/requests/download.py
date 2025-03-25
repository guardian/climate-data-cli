import os
import tempfile
import datapi
import shutil


class CdsDownload:
    def __init__(self, client: datapi.ApiClient, job_id: str):
        self._client = client
        self._job_id = job_id

    def __enter__(self):
        self._temp_file = tempfile.NamedTemporaryFile()
        self._temp_dir = tempfile.TemporaryDirectory()

        return self

    def download(self):
        self.remote = self._client.get_remote(self._job_id)

        self._client.get_remote(self._job_id).download(self._temp_file.name)

        shutil.unpack_archive(self._temp_file.name, self._temp_dir.name, format="zip")

        extracted_files = [
            os.path.join(self._temp_dir.name, file)
            for file in os.listdir(self._temp_dir.name)
        ]

        self.downloaded_files = sorted(extracted_files)

        self.downloaded_files_types = {
            os.path.splitext(file)[1] for file in self.downloaded_files
        }

    def get_file_paths(self):
        return self.downloaded_files

    def get_file_types(self):
        downloaded_files_types = {
            os.path.splitext(file)[1] for file in self.downloaded_files
        }

        return list(downloaded_files_types)

    def is_downloaded(self):
        return hasattr(self, "downloaded_files")

    def __exit__(self, type, value, traceback):
        self._temp_file.close()
        self._temp_dir.cleanup()
