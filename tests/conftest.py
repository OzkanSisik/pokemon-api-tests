import pytest
from api.pokemon_api import PokemonAPI
from config.settings import BASE_URL


@pytest.fixture(scope="session")
def pokemon_api():
    return PokemonAPI()
