import pytest
from api.pokemon_api import PokemonAPI
from utils import wait_for_service
from config.settings import BASE_URL


@pytest.fixture(scope="session")
def pokemon_api():
    return PokemonAPI()


@pytest.fixture(scope='session', autouse=False)
def wait_mock_service():
    wait_for_service(BASE_URL)
