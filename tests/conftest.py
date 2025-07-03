import pytest
from api.pokemon_api import PokemonAPI
from utils import get_base_url


@pytest.fixture(scope="session")
def pokemon_api():
    return PokemonAPI()


@pytest.fixture(scope="session")
def api_base_url():
    return get_base_url()