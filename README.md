Sem problemas! Aqui está o README final, completinho e estilizado para você copiar e colar. Ele já inclui os escudos (badges), a tabela de endpoints e as instruções de segurança.

Basta substituir o conteúdo do seu arquivo README.md por este:

Markdown
# EBAC PokeBackend PRO 🚀

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-05998b.svg)
![Tests](https://img.shields.io/github/actions/workflow/status/jterzian/EBAC-PokeBackend/main.yml?branch=main&label=tests)
![Deploy](https://img.shields.io/badge/deploy-Render-430098.svg)

Esta é uma API robusta desenvolvida como projeto final para o curso de Backend Python da **EBAC**. O sistema consome a PokéAPI oficial, aplica filtros inteligentes, validação de dados e camadas de segurança profissional.

## 🔗 Links do Projeto
- **API em Produção:** [https://ebac-pokebackend.onrender.com/docs](https://ebac-pokebackend.onrender.com/docs)
- **Documentação:** Swagger UI integrada.

---

## 🔒 Segurança e Autenticação
Para garantir a integridade dos dados, os endpoints de Pokémons são protegidos por uma **API Key**.

* **Header Key:** `access_token`
* **Token de Acesso:** `ebac-token-2024`

> **Como testar:** No Swagger UI, clique no botão verde **"Authorize"**, insira o token acima e clique em autorizar.

## 🚦 Rate Limiting (Controle de Tráfego)
Implementamos uma barreira de segurança contra abusos (Rate Limit):
* **Limite:** 5 requisições por minuto por IP.
* **Status de Erro:** `429 Too Many Requests`.

---

## 📡 Endpoints Disponíveis

| Método | Rota | Descrição | Autenticação |
| :--- | :--- | :--- | :---: |
| **GET** | `/` | Status da API e mensagem de boas-vindas | ❌ |
| **GET** | `/pokemons` | Listagem paginada (limit/offset) | ✅ |
| **GET** | `/pokemons/{id}` | Detalhes filtrados de um Pokémon específico | ✅ |

---

## 🛠️ Tecnologias e Opcionais Implementados
- [x] **Pydantic:** Validação rigorosa dos tipos de dados.
- [x] **Logs Estruturados:** Monitoramento de acessos no servidor.
- [x] **Tratamento de Exceções:** Erros 404 e 403 customizados.
- [x] **CI/CD:** Pipeline automatizado com GitHub Actions (Pytest).
- [x] **Docker:** Containerização pronta para produção.

## 🐳 Como Executar Localmente

### Via Docker (Recomendado)
```bash
docker-compose up --build
A API ficará disponível em http://localhost:8000/docs

Via Python Direto
Instale as dependências: pip install -r requirements.txt

Rode o servidor: uvicorn app.main:app --reload

🧪 Testes Unitários
Para rodar os testes e verificar a integridade da autenticação e paginação:

Bash
pytest