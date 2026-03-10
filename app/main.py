import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
from typing import List, Optional

# --- CONFIGURAÇÃO DE LOGS ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PokeAPI-Ebac")

app = FastAPI(
    title="EBAC PokeBackend", 
    description="API filtrada da PokéAPI com Pydantic, Logs e CI/CD",
    version="1.0.0"
)

# --- CONFIGURAÇÃO DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS PYDANTIC (Validação de Dados) ---
class PokemonSummary(BaseModel):
    name: str
    url: str

class PokemonListResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PokemonSummary]

class PokemonDetail(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    types: List[str]
    sprite: str

# --- ENDPOINTS ---

@app.get("/", tags=["Root"])
async def read_root():
    logger.info("Endpoint Root acessado")
    # A frase abaixo DEVE ser exatamente esta para passar no seu teste unitário
    return {"message": "PokeAPI Wrapper da EBAC está online!"}

@app.get("/pokemons", response_model=PokemonListResponse, tags=["Pokemons"])
async def list_pokemons(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    logger.info(f"Listagem solicitada: limit={limit}, offset={offset}")
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Erro ao acessar PokeAPI: {e}")
            raise HTTPException(status_code=500, detail="Erro ao buscar lista de Pokémons")

@app.get("/pokemons/{pokemon_id}", response_model=PokemonDetail, tags=["Pokemons"])
async def get_pokemon_detail(pokemon_id: str):
    logger.info(f"Busca detalhada do pokemon: {pokemon_id}")
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id.lower()}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
        if response.status_code == 404:
            logger.warning(f"Pokemon não encontrado: {pokemon_id}")
            raise HTTPException(
                status_code=404, 
                detail=f"Pokémon '{pokemon_id}' não encontrado na base de dados oficial."
            )
        
        data = response.json()
        
        # Filtragem seletiva dos dados conforme requisito do projeto
        filtered_data = {
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "sprite": data["sprites"]["front_default"] or ""
        }
        return filtered_data