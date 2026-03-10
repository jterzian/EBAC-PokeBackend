from pydantic import BaseModel
from typing import List, Optional

class PokemonSchema(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    types: List[str]
    sprite: str

class PokemonListResponse(BaseModel):
    total: int
    next: Optional[str]
    previous: Optional[str]
    results: List[dict]