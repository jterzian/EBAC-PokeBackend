import httpx

BASE_URL = "https://pokeapi.co/api/v2/pokemon"

class PokeService:
    @staticmethod
    async def get_pokemon_details(pokemon_id_or_name: str):
        """Busca detalhes de um Pokémon específico e formata os dados para o Schema"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{BASE_URL}/{pokemon_id_or_name.lower()}")
                if response.status_code == 200:
                    data = response.json()
                    # Retornamos o dicionário formatado exatamente como o schemas.PokemonDetail espera
                    return {
                        "id": data["id"],
                        "name": data["name"],
                        "height": data["height"],
                        "weight": data["weight"],
                        "types": [t["type"]["name"] for t in data["types"]],
                        "sprite": data["sprites"]["front_default"]
                    }
                return None
            except Exception:
                return None