from sqlalchemy import Column, Integer, String
from .database import Base

class PokemonModel(Base):
    __tablename__ = "my_pokemons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    note = Column(String, nullable=True)