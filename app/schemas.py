from pydantic import BaseModel, ConfigDict
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
    # Novo padrão do Pydantic V2 para substituir o 'class Config'
    model_config = ConfigDict(from_attributes=True)