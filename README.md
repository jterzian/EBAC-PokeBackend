# EBAC - PokeBackend Wrapper

Projeto desenvolvido como parte do curso de Backend Python da EBAC. Esta API consome dados da PokéAPI, filtra informações relevantes e expõe via FastAPI.

## 🚀 Tecnologias
* Python 3.11+
* FastAPI
* Docker & Docker Compose
* Pytest (Testes Unitários)
* GitHub Actions (CI/CD)

## 📦 Como rodar com Docker
1. Clone o repositório:
   `git clone https://github.com/SEU_USUARIO/EBAC-PokeBackend.git`
2. Na raiz do projeto, rode:
   `docker-compose up --build`
3. Acesse a documentação:
   `http://localhost:8000/docs`

## 🧪 Como rodar testes
```bash
pytest tests/

---

### Checklist de Revisão Final:
Antes de dar o `git push`, confirme se sua árvore de arquivos está assim:
```text
EBAC-PokeBackend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── services.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── main.yml
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md