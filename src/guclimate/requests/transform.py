import xarray as xr
from typing import Literal
from .download import CdsDownload
from cfgrib.xarray_to_grib import to_grib
import xcdat
import os
import shutil


class CdsTransformer:
    def __init__(self, download: CdsDownload):
        if not download.is_downloaded():
            raise ValueError(
                "CdsDownload must have downloaded data to be given to converter"
            )

        self.download = download

    def __enter__(self):
        file_types = self.download.get_file_types()

        if len(file_types) > 1:
            raise ValueError(
                f"Multiple file types found in downloaded files: {
                    ', '.join(file_types)}"
            )

        if file_types[0] != ".grib":
            raise ValueError(
                f"Downloading '{file_types[0]}' is not currently supported"
            )

        return self

    def save_as(self, type: Literal["csv", "ncdf", "grib"], filename: str):
        if type == "csv":
            self._load_as_grib()
            return self._save_as_csv(filename)
        elif type == "grib":
            return self._save_as_grib(filename)
        elif type == "nc":
            self._load_as_grib()
            return self._save_as_ncdf(filename)

    def _save_as_csv(self, filename: str):
        self.data.to_dataframe().to_csv(filename)
        return create_save_info_dict(filename, 1)

    def _save_as_grib(self, filename: str):
        # For now we assume that only .grib files come from the API, so we don't need to load
        # anything into memory, only move the files from the archive

        if len(self.download.get_file_paths()) == 1:
            shutil.copy(self.download.get_file_paths()[0], filename)
            return create_save_info_dict(filename, 1)

        filename_wo_extension = filename.split(".")[0]

        os.makedirs(filename_wo_extension, exist_ok=True)

        for file in self.download.get_file_paths():
            shutil.copy(file, filename_wo_extension)

        return create_save_info_dict(
            filename_wo_extension, len(self.download.get_file_paths())
        )

    def _save_as_ncdf(self, filename: str):
        self.data.to_netcdf(filename)
        return create_save_info_dict(filename, 1)

    def _load_as_grib(self):
        datasets = [
            xr.open_dataset(file, engine="cfgrib", decode_timedelta=False)
            for file in self.download.get_file_paths()
        ]

        self.data = xr.concat(datasets, dim="time")

        self.data = xcdat.swap_lon_axis(self.data, (-180, 180))

    def __exit__(self, type, value, traceback):
        pass


def create_save_info_dict(filename: str, files_created: int):
    return {
        "filename": filename,
        "files_created": files_created,
    }
