import pytest
from api.pokemon_api import PokemonAPI


@pytest.fixture(scope="session")
def pokemon_api():
    return PokemonAPI()
