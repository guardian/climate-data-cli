import typer
import cdsapi

client = cdsapi.Client()


def main():
    client = cdsapi.Client()
    client.retrieve(
        "ecv-for-climate-change",
        {
            "variable": "surface_air_temperature",
            "product_type": "anomaly",
            "climate_reference_period": "1991_2020",
            "time_aggregation": "1_month_mean",
            "year": [
                "2022",
                "2023",
            ],
            "month": [
                "01",
                "02",
            ],
            "origin": "era5",
            "format": "zip",
        },
        "download.zip",
    )


if __name__ == "__main__":
    typer.run(main)
