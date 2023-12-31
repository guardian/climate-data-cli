import xcdat
import pprint
import xarray as xr
import pandas

pp = pprint.PrettyPrinter(indent=2)

# Convert temperature units from Kelvin to Celsius
# Temperature anomalies should not be converted, because relative temperatures are the same in Kelvin and Celsius
# da_degc = da - 273.15

# Assign attributes to new data array, and change the unit
# da_degc = da_degc.assign_attrs(da.attrs)
# da_degc.attrs['units'] = '°C'


def open_dataset(path):
    # Open file and ensure longitude is encoded as [-180, 180] range instead of [0, 360]
    ds = xcdat.open_dataset(path, lon_orient=(-180, 180))

    return Dataset(ds)


class Dataset:
    def __init__(self, ds) -> None:
        self.ds = ds

    def global_mean(self, variable: str):
        global_avg = self.ds.spatial.average(variable)
        return Dataset(global_avg)

    def timeseries(self, variable: str) -> pandas.DataFrame:
        dr = xr.DataArray(
            self.ds[variable], coords=[self.ds.coords["time"]], dims=["time"]
        )
        return dr.to_dataframe()

    def inspect(self):
        pp.pprint(self.ds)
