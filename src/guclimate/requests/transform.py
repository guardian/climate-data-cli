import pdb
import xarray as xr
from typing import Literal

from .download import CdsDownload


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
                f"Multiple file types found in downloaded files: {', '.join(file_types)}"
            )

        if file_types[0] == ".grib":
            self._load_as_grib()
        else:
            raise ValueError(
                f"Downloading '{file_types[0]}' is not currently supported"
            )

        return self

    def save_as(self, type: Literal["csv"], filename: str):
        if getattr(self, "data") is None:
            raise ValueError("Data must be loaded before converting")

        if type == "csv":
            self._save_as_csv(filename)

        pass

    def _save_as_csv(self, filename: str):
        self.data.to_dataframe().to_csv(filename)

    def _load_as_grib(self):
        datasets = [
            xr.open_dataset(file, engine="cfgrib", decode_timedelta=False)
            for file in self.download.get_file_paths()
        ]

        self.data = xr.concat(datasets, dim="time")

    def __exit__(self, type, value, traceback):
        pass
