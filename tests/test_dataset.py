from src.guclimate.core import dataset

def test_open_file():
    ds = dataset.open_dataset(
        "tests/data/precipitation/anomalies-monthly-means-2022.nc"
    )
    assert type(ds) is dataset.Dataset