# 🚀 PokeBackend EBAC - Projeto Final

Este projeto é um **Backend robusto** desenvolvido em Python com FastAPI, que funciona como um wrapper para a PokéAPI externa, mas também possui sua própria camada de persistência de dados (CRUD Local).

## 🛠️ O que foi implementado? (Destaques Técnicos)

- **Persistência com SQLAlchemy 2.0**: Integração com banco de dados SQLite para salvar, listar e deletar Pokémons customizados.
- **Segurança (API Key)**: Endpoints protegidos por autenticação via Header (`access_token`).
- **Arquitetura em Camadas**: Organização profissional dividida em `models`, `schemas`, `services`, `utils` e `database`.
- **Assincronismo**: Uso de `httpx` para chamadas externas eficientes e não bloqueantes.
- **Validação Rigorosa**: Uso do Pydantic V2 para garantir a integridade dos dados.
- **CI/CD Integrado**: Pipeline no GitHub Actions que executa testes automatizados (Pytest) a cada push.

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/jterzian/EBAC-PokeBackend.git](https://github.com/jterzian/EBAC-PokeBackend.git)
   cd EBAC-PokeBackend
Configure o ambiente:
Crie um arquivo .env na raiz com as seguintes chaves:

Snippet de código
API_KEY=ebac-token-2024
DATABASE_URL=sqlite:///./test.db
APP_TITLE=PokeBackend-EBAC
Instale as dependências:

Bash
pip install -r requirements.txt
Inicie o servidor:

Bash
uvicorn app.main:app --reload
Acesse a documentação em: http://127.0.0.1:8000/docs

🧪 Testes Automatizados
Para rodar os testes de integração e garantir que tudo está funcionando:

Bash
pytest
🔗 Deploy
O projeto está configurado para deploy automático no Render e pode ser acessado publicamente através da URL fornecida no repositório.

Desenvolvido por João como parte do curso de Python Backend da EBAC.
