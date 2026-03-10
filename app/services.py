import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon"

class PokeService:
    @staticmethod
    def get_pokemon_list(limit: int = 20, offset: int = 0):
        """Busca a lista paginada de Pokémons"""
        response = requests.get(f"{BASE_URL}?limit={limit}&offset={offset}")
        if response.status_code == 200:
            data = response.json()
            return {
                "total": data["count"],
                "next": data["next"],
                "previous": data["previous"],
                "results": data["results"]
            }
        return None

    @staticmethod
    def get_pokemon_details(pokemon_id_or_name: str):
        """Busca detalhes de um Pokémon específico e filtra os dados"""
        response = requests.get(f"{BASE_URL}/{pokemon_id_or_name}")
        if response.status_code == 200:
            data = response.json()
            return {
                "id": data["id"],
                "name": data["name"],
                "height": data["height"],
                "weight": data["weight"],
                "types": [t["type"]["name"] for t in data["types"]],
                "sprite": data["sprites"]["front_default"]
            }
        return None