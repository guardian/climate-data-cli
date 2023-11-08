import xarray as xr

# Convert temperature units from Kelvin to Celsius
# Temperature anomalies should not be converted, because relative temperatures are the same in Kelvin and Celsius
# da_degc = da - 273.15

# Assign attributes to new data array, and change the unit
# da_degc = da_degc.assign_attrs(da.attrs)
# da_degc.attrs['units'] = '°C'

def open_dataset(path):
    ds = xr.open_dataset(path, engine='cfgrib')

    # Check if longitude is encoded as [0, 360] range instead of [-180, 180]
    longitude = ds.coords['longitude'].values
    if max(longitude) > 180:
        # Convert longitude to [-180, 180] range
        ds = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180)).sortby('longitude')

    return Dataset(ds['t2m'])

class Dataset:
    def __init__(self, ds) -> None:
        self.ds = ds

    def global_mean():
        


    
        