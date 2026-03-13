import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

# Define o header de autenticação baseado no que está no seu .env ou padrão
API_KEY = os.getenv("API_KEY", "ebac-token-2024")
HEADERS = {"access_token": API_KEY}

def test_read_root():
    """Testa o endpoint raiz com a nova mensagem"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Bem-vindo ao PokeBackend EBAC!" in response.json()["message"]

def test_get_external_pokemon_success():
    """Testa a busca de um pokemon real na PokeAPI com token"""
    response = client.get("/pokemons/pikachu", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["name"] == "pikachu"

def test_unauthorized_access():
    """Testa se a API nega acesso sem o token correto"""
    response = client.get("/pokemons/pikachu", headers={"access_token": "token-errado"})
    assert response.status_code == 403

def test_create_local_pokemon():
    """Testa a criação de um pokemon no banco de dados local (CRUD)"""
    payload = {
        "name": "Ebac-Test",
        "type": "Eletrico",
        "note": "Teste de Unidade"
    }
    response = client.post("/my-pokemons", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ebac-Test"
    assert "id" in data

def test_list_local_pokemons():
    """Testa a listagem do banco local"""
    response = client.get("/my-pokemons", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)