import unittest
from src.guclimate.core import dataset

class TestCore(unittest.TestCase):
    def test_open_file(self):
        ds = dataset.open_dataset(
            "tests/data/precipitation/anomalies-monthly-means-2022.nc"
        )
        self.assertIsInstance(ds, dataset.Dataset)


class TestPrecipitationAnomalies(unittest.TestCase):
    def test_something(self):
        self.assertEqual(5, 5)


if __name__ == "__main__":
    unittest.main()
