import os
def test_get_pikachu(pokemon_api):
    response = pokemon_api.get_pokemon("pikachu")
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'pikachu'
    assert "static" in data['abilities']


def test_get_bulbasaur(pokemon_api):
    response = pokemon_api.get_pokemon("bulbasaur")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "bulbasaur"


def test_get_invalid_pokemon(pokemon_api):
    response = pokemon_api.get_pokemon("notapokemon")
    assert response.status_code == 404


def test_get_ability(pokemon_api):
    response = pokemon_api.get_ability("static")
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'static'
    assert 'description' in data
