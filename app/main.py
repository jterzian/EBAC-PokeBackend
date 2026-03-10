import logging
from fastapi import FastAPI, HTTPException, Query, Security, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
import httpx
from pydantic import BaseModel
from typing import List, Optional

# --- BIBLIOTECAS DE RATE LIMIT ---
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# --- CONFIGURAÇÃO DE LOGS ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PokeAPI-Ebac")

# --- CONFIGURAÇÃO DO RATE LIMIT ---
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="EBAC PokeBackend PRO",
    description="API com Pydantic, Logs, Rate Limit e Auth",
    version="1.1.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CONFIGURAÇÃO DE AUTENTICAÇÃO ---
API_KEY = "ebac-token-2024"
api_key_header = APIKeyHeader(name="access_token", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=403, 
        detail="Acesso negado: API Key inválida ou ausente no header 'access_token'"
    )

# --- CONFIGURAÇÃO DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS PYDANTIC ---
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
@limiter.limit("5/minute")
async def read_root(request: Request):
    logger.info("Endpoint Root acessado")
    return {"message": "PokeAPI Wrapper da EBAC está online!"}

@app.get("/pokemons", response_model=PokemonListResponse, tags=["Pokemons"])
@limiter.limit("5/minute")
async def list_pokemons(
    request: Request, 
    limit: int = Query(20, ge=1, le=100), 
    offset: int = Query(0, ge=0),
    token: str = Depends(get_api_key)
):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

@app.get("/pokemons/{pokemon_id}", response_model=PokemonDetail, tags=["Pokemons"])
@limiter.limit("5/minute")
async def get_pokemon_detail(
    request: Request, 
    pokemon_id: str,
    token: str = Depends(get_api_key)
):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id.lower()}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, 
                detail=f"Pokémon '{pokemon_id}' não encontrado na base de dados oficial."
            )
        
        data = response.json()
        return {
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "sprite": data["sprites"]["front_default"] or ""
        }