from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="EBAC-PokeBackend", version="0.1.0")

# --- RESOLVE O ERRO DE CARREGAMENTO ETERNO (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://pokeapi.co/api/v2/pokemon"

@app.get("/")
def read_root():
    return {"message": "PokeAPI Wrapper da EBAC está online!"}

# --- ENDPOINT DE LISTAGEM COM PAGINAÇÃO (EXIGIDO PELO PROFESSOR) ---
@app.get("/pokemons")
def list_pokemons(
    limit: int = Query(default=10, ge=1, le=100), 
    offset: int = Query(default=0, ge=0)
):
    try:
        response = requests.get(f"{BASE_URL}?limit={limit}&offset={offset}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Erro ao conectar com a PokeAPI")

# --- ENDPOINT DE BUSCA POR ID/NOME COM FILTRO DE DADOS ---
@app.get("/pokemons/{pokemon_id}")
def get_pokemon(pokemon_id: str):
    try:
        response = requests.get(f"{BASE_URL}/{pokemon_id.lower()}")
        
        # --- TRATAMENTO DE ERRO 404 (TESTADO COM AGUMON) ---
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Pokémon não encontrado")
            
        data = response.json()
        
        # --- FILTRAGEM DE DADOS (REQUISITO OBRIGATÓRIO) ---
        pokemon_info = {
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "sprite": data["sprites"]["front_default"]
        }
        return pokemon_info

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
