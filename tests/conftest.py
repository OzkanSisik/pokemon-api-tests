import pytest
import os
from api.pokemon_api import PokemonAPI
from utils import wait_for_service, get_base_url


@pytest.fixture(scope="session")
def pokemon_api():
    return PokemonAPI()


@pytest.fixture(scope='session', autouse=True)
def wait_mock_service():
    """
    Wait for the mock service to be ready before running any tests.
    This fixture runs automatically for all tests.
    """
    base_url = get_base_url()
    wait_for_service(base_url)
    return base_url


@pytest.fixture(scope="session")
def api_base_url(wait_mock_service):
    """
    Provide the base URL for API tests
    """
    return wait_mock_service