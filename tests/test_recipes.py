import pytest
import yaml
from src.guclimate.core.recipe import Recipe, Retrieval

@pytest.mark.datafiles("sample-recipes/get_monthly_mean_temp_since_1940.yaml")
def test_get_retrievals(datafiles):
    for file in datafiles.iterdir():
        yaml_recipe = yaml.safe_load(file.read_text())
        recipe = Recipe(yaml_recipe)
        assert len(recipe.retrievals()) == 1
        assert type(recipe.retrievals()[0]) is Retrieval
