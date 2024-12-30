## Prequisites

* Conda package manager (installed through [miniforge](https://github.com/conda-forge/miniforge))

The easiest way to install miniforge on MacOS is using Homebrew: `brew install miniforge`. Alternatively, you can download and run an installer the appropriate installer for your platform from the [miniforge repository](https://github.com/conda-forge/miniforge).

## Installation

1. Clone this repo
2. Navigate to the project directory using the command line prompt
3. Run `conda env create --file ./environment.yml` to install dependencies in a virtual environment
4. Activate the virtual environment: `conda activate climate-data`
5. Install Python packages `python -m pip install -r requirements.txt`

## Getting started

### Set up credentials

To retrieve data from the [Climate Data Store](https://cds.climate.copernicus.eu/), you need to create an ECMWF account first. Once you have created the account, log in and go to your profile page, where you'll find your API token.

Create a `~/.datapirc` conguration file, and paste the following, replacing the key with your API token from the previous step.
> Note: this project uses the newer [datapi](https://github.com/ecmwf-projects/datapi?tab=readme-ov-file) package instead of [cdsapi](https://github.com/ecmwf/cdsapi)


```
url: https://cds.climate.copernicus.eu/api
key: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```


With the tool installed you can now run `guclimate retrieve verify`. And you should see output similar to this:
```
Verifying CDS credentials
Credentials verified {...}
```

## Development

### Install the module for local development

Install the guclimate CLI from source:
1. Make sure you're in the project directory
2. Run `pip install -e .`

You should now be able to run the tool. Try:
```
guclimate --help
```

### Adding a non-Python dependency

* To add a new dependency, add it to environment.yml and run the following command in the project directory:

```
conda env update --file environment.yml --prune
```

### Running tests

```
python -m run_tests
```

## API

To retrieve data from the CDS api and process it, you need to create a recipe. Recipes are written in [YAML](https://yaml.org/).

At its most basic, a recipe consists of a name and a description. For example:

```yaml
---
name: "Daily temperatures 2024"
description: "Get daily temperatures (global mean) for 2024"
```

To retrieve CDS data, define a new key under the `retrieve` keyword, to refer to your dataset. In this case we'll call it `daily_mean_temp`:

```yaml
---
name: "Daily temperatures 2024"
description: "Get daily temperatures (global mean) for 2024"
retrieve:
  daily_mean_temp:
```

Next we need to define the parameters for the data we want to retrieve. The parameter names and values should match what you find in the [CDS web interface](https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics?tab=download) (click _Show API Request Code_).

For instance, this is what we would find in the web interface:

```python
import cdsapi

dataset = "derived-era5-single-levels-daily-statistics"
request = {
    "product_type": "reanalysis",
    "variable": ["2m_temperature"],
    "daily_statistic": "daily_mean",
    "time_zone": "utc+00:00",
    "frequency": "1_hourly"
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
```

And this is what it looks like in our recipe:

```yaml
---
name: "Daily temperatures chart"
description: "Get daily temperatures (global mean) for 2024"
retrieve:
  daily_mean_temp:
    product: derived-era5-single-levels-daily-statistics
    product_type: reanalysis
    variable: 2m_temperature
    daily_statistic: daily_mean
    time_zone: "utc+00:00"
    frequency: 1_hourly
```

We also need to define the timeframe that we're interested in, using the `year`, `month` and `day` parameters. These parameters are treated slightly differently, so that we can simply write:

```yaml
month: 1-12
```

rather than:

```yaml
month: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
```

Here's what our recipe looks like when we add those parameters:

```yaml
---
name: "Daily temperatures chart"
description: "Get daily temperatures (global mean) for 2024"
retrieve:
  daily_mean_temp:
    product: derived-era5-single-levels-daily-statistics
    product_type: reanalysis
    variable: 2m_temperature
    daily_statistic: daily_mean
    time_zone: "utc+00:00"
    frequency: 1_hourly
    year: 2024
    month: 1-12
    day: 1-31
```