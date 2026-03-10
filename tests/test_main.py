from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "PokeAPI Wrapper da EBAC está online!"}

def test_get_pokemon_valid():
    response = client.get("/pokemons/pikachu")
    assert response.status_code == 200
    assert response.json()["name"] == "pikachu"

def test_get_pokemon_invalid():
    response = client.get("/pokemons/pokemon-inexistente")
    assert response.status_code == 404