from api.base_api import BaseAPI


class PokemonAPI(BaseAPI):
    def get_pokemon(self, name_or_id):
        endpoint = f"/pokemon/{name_or_id}"
        return self.get(endpoint)

    def get_ability(self, ability_name):
        endpoint = f"/ability/{ability_name}"
        return self.get(endpoint)

    def get_pokemon_by_id(self, pokemon_id):
        endpoint = f"/pokemons/{pokemon_id}"
        return self.get(endpoint)
