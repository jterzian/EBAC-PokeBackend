from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# A mesma chave que definimos no main.py
HEADERS = {"access_token": "ebac-token-2024"}

def test_read_root():
    """Testa o endpoint raiz (que tem rate limit mas não exige token)"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "PokeAPI Wrapper da EBAC está online!"}

def test_list_pokemons():
    """Testa a listagem paginada enviando o token de acesso"""
    response = client.get("/pokemons?limit=5&offset=0", headers=HEADERS)
    assert response.status_code == 200
    assert "results" in response.json()
    assert len(response.json()["results"]) == 5

def test_get_pokemon_detail():
    """Testa a busca de um pokemon específico enviando o token"""
    response = client.get("/pokemons/pikachu", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["name"] == "pikachu"
    assert "id" in response.json()

def test_get_pokemon_not_found():
    """Testa o erro 404 enviando o token"""
    response = client.get("/pokemons/pokemon-inexistente", headers=HEADERS)
    assert response.status_code == 404

def test_unauthorized_access():
    """Testa se a API nega acesso sem o token (Erro 403)"""
    response = client.get("/pokemons/pikachu")
    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso negado: API Key inválida ou ausente no header 'access_token'"