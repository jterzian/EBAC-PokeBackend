# ⚡ EBAC-PokeBackend

Projeto final do curso de Backend Python da EBAC. Esta API foi desenvolvida com **FastAPI** e consome a **PokeAPI** oficial, aplicando filtros de dados, paginação e práticas modernas de DevOps.

## 🚀 Demonstração
- **API Live:** [https://ebac-pokebackend.onrender.com/docs](https://ebac-pokebackend.onrender.com/docs)
- **Documentação:** Swagger UI nativo disponível no endpoint `/docs`.

## 🛠️ Tecnologias e Recursos Utilizados
- **Linguagem:** Python 3.11
- **Framework:** FastAPI (Assíncrono)
- **Validação de Dados:** Pydantic
- **Containerização:** Docker & Docker Compose
- **Testes:** Pytest (Cobertura de endpoints e lógica)
- **CI/CD:** GitHub Actions (Automação de testes e Deploy contínuo no Render)

## 📋 Funcionalidades Implementadas
- [x] **Listagem Paginada:** Endpoint `/pokemons` com parâmetros `limit` e `offset`.
- [x] **Busca Específica:** Endpoint `/pokemons/{id_or_name}` com filtragem seletiva de atributos.
- [x] **Tratamento de Erros:** Exceções customizadas para Pokémons não encontrados (404).
- [x] **CORS:** Configurado para permitir requisições de diferentes origens.
- [x] **Documentação Automática:** Swagger e ReDoc.

## 📦 Como Rodar o Projeto Localmente

### Via Docker (Recomendado)
1. Certifique-se de ter o Docker instalado.
2. Clone o repositório:
   ```bash
   git clone [https://github.com/jterzian/EBAC-PokeBackend.git](https://github.com/jterzian/EBAC-PokeBackend.git)
Execute o comando:

Bash
docker-compose up --build
Acesse http://localhost:8000/docs.

Via Ambiente Virtual (Manual)
Crie um venv: python -m venv venv

Instale as dependências: pip install -r requirements.txt

Rode a aplicação: uvicorn main:app --reload

🧪 Executando Testes
Para garantir a estabilidade, execute os testes unitários com:

Bash
pytest
Os testes cobrem: sucesso na listagem, funcionamento da paginação e erro 404.

⚙️ CI/CD e Deploy
O projeto utiliza GitHub Actions. Toda vez que um código é enviado para a branch main:

O pipeline de CI é acionado.

Os testes unitários são executados.

Se aprovado, o deploy é feito automaticamente no Render.


---

### 3. O "Pulo do Gato" para os Opcionais no Código

Se você quiser garantir que o **Pydantic** e os **Logs** apareçam como "Feitos", verifique se seu `main.py` tem algo parecido com isso:

```python
import logging
from pydantic import BaseModel

# Configuração de Log Estruturado (Opcional)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelo Pydantic (Opcional/Requisito técnico)
class PokemonSchema(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    types: list
    sprite: str

# No seu endpoint:
@app.get("/pokemons/{pokemon_id}", response_model=PokemonSchema)
async def get_pokemon(pokemon_id: str):
    logger.info(f"Buscando informações do pokemon: {pokemon_id}")
    # ... sua lógica ...