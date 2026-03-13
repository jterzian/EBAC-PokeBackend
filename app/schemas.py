from pydantic import BaseModel
from typing import List, Optional

# Schemas para a PokeAPI (Externo)
class PokemonSummary(BaseModel):
    name: str
    url: str

class PokemonListResponse(BaseModel):
    count: int
    results: List[PokemonSummary]

class PokemonDetail(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    types: List[str]
    sprite: str

# Schemas para o CRUD Local (SQLAlchemy)
class PokemonCreate(BaseModel):
    name: str
    type: str
    note: Optional[str] = None

class PokemonDB(PokemonCreate):
    id: int
    class Config:
        from_attributes = True