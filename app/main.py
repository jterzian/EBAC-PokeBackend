from fastapi import FastAPI, HTTPException, Query
from app.services import PokeService
from app.schemas import PokemonSchema

app = FastAPI(title="EBAC-PokeBackend")

@app.get("/")
def read_root():
    return {"message": "PokeAPI Wrapper da EBAC está online!"}

# Endpoint de Listagem Paginada
@app.get("/pokemons")
def list_pokemons(limit: int = 20, offset: int = 0):
    data = PokeService.get_pokemon_list(limit, offset)
    if not data:
        raise HTTPException(status_code=500, detail="Erro ao acessar a PokéAPI")
    return data

# Endpoint de Detalhes por ID ou Nome
@app.get("/pokemons/{pokemon_id}", response_model=PokemonSchema)
def get_pokemon(pokemon_id: str):
    pokemon = PokeService.get_pokemon_details(pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    return pokemon