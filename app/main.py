import os
from typing import List
from fastapi import FastAPI, HTTPException, Depends, Security, Request
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Importando seus módulos organizados
from . import models, database, schemas, services, utils
from .database import engine, get_db

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Cria as tabelas no banco de dados local (test.db) se não existirem
models.Base.metadata.create_all(bind=engine)

# 3. Configurações de Segurança e Título vindas do .env
API_KEY = os.getenv("API_KEY")
APP_TITLE = os.getenv("APP_TITLE", "PokeBackend EBAC")
api_key_header = APIKeyHeader(name="access_token", auto_error=False)

app = FastAPI(title=APP_TITLE)

# Dependência para verificar a API Key
async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=403, 
        detail="Acesso negado: API Key inválida ou ausente no header 'access_token'"
    )

# --- ENDPOINT RAIZ ---
@app.get("/", tags=["Geral"])
async def read_root():
    return {"message": f"Bem-vindo ao {APP_TITLE}! Acesse /docs para testar os endpoints."}

# --- POKEAPI (Consumo Externo via Service) ---
@app.get("/pokemons/{pokemon_id}", response_model=schemas.PokemonDetail, tags=["PokeAPI Externa"])
async def get_external_pokemon(pokemon_id: str, _ = Depends(verify_api_key)):
    # Formata o nome usando sua função no utils.py
    formatted_id = utils.format_pokemon_name(pokemon_id)
    
    # Busca os detalhes usando o PokeService que você criou
    data = await services.PokeService.get_pokemon_details(formatted_id)
    
    if not data:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado na PokeAPI externa")
    
    # O service já retorna os dados, mas aqui garantimos o mapeamento para o response_model
    return data

# --- MEU CRUD (Banco de Dados Local com SQLAlchemy) ---

@app.post("/my-pokemons", response_model=schemas.PokemonDB, tags=["Meu CRUD Local"])
def create_local_pokemon(
    pokemon: schemas.PokemonCreate, 
    db: Session = Depends(get_db), 
    _ = Depends(verify_api_key)
):
    """Cria um novo Pokémon no seu banco de dados próprio"""
    db_pokemon = models.PokemonModel(**pokemon.model_dump())
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon

@app.get("/my-pokemons", response_model=List[schemas.PokemonDB], tags=["Meu CRUD Local"])
def list_local_pokemons(db: Session = Depends(get_db), _ = Depends(verify_api_key)):
    """Lista todos os Pokémons salvos no seu banco de dados"""
    return db.query(models.PokemonModel).all()

@app.delete("/my-pokemons/{id}", tags=["Meu CRUD Local"])
def delete_local_pokemon(id: int, db: Session = Depends(get_db), _ = Depends(verify_api_key)):
    """Remove um Pokémon do seu banco de dados local"""
    pokemon = db.query(models.PokemonModel).filter(models.PokemonModel.id == id).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado no banco local")
    db.delete(pokemon)
    db.commit()
    return {"status": "sucesso", "message": f"Pokémon com ID {id} foi removido."}