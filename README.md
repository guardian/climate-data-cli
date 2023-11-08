## Prequisites

* Conda package manager (installed through [miniforge](https://github.com/conda-forge/miniforge))

The easiest way to install miniforge on MacOS is using Homebrew: `brew install miniforge`. Alternatively, you can download and run an installer the appropriate installer for your platform from the [miniforge repository](https://github.com/conda-forge/miniforge).

## How to use

1. Clone this repo
2. Navigate to the project directory using the command line prompt
3. Run `mamba env create -p ./.env --file ./environment.yml` to install dependencies in a virtual environment
4. Activate the virtual environment: `conda activate ./.env`
5. Install Python packages `python -m pip install -r requirements.txt`

## Development

* To add a new dependency, add it to environment.yml and run the following command in the project directory:

```
mamba env update --file ./environment.yml -p ./.env --prune
```