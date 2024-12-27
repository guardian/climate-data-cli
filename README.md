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

### Creating your first recipe



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
