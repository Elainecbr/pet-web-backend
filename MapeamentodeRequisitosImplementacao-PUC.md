# Mapeamento de Requisitos -> Implementação

Este arquivo relaciona os requisitos do PDF "Requisitos para o MVP" com os arquivos/rotas implementadas neste projeto.

Resumo dos requisitos observados (do enunciado do curso)
- Backend: 4.0 pontos — API REST com CRUD básico, documentação (Swagger/OpenAPI), persistência (SQLite).
- Frontend: 4.0 pontos — SPA estática que consome a API, UX mínima (cadastro/login leve, registro de pet, visualização).
- Organização: 2.0 pontos — separação em dois repositórios (frontend e backend), READMEs explicativos e instruções para rodar.

Mapeamento (requisito -> implementação / arquivos)

- Servir SPA na raiz (para testes locais):
  - Implementado em `backend/app.py` com rota catch-all que serve os estáticos do diretório `frontend/` quando aplicável.

- Documentação OpenAPI / Swagger:
  - Especificação: `backend/swagger.yaml`
  - Swagger UI: `GET /swagger` (registrado em `app.py`); `GET /swagger.yaml` serve o arquivo YAML.

- Endpoints principais (exigidos para a demo / pontos):
  - `GET /racas` — lista raças. Implementação: `backend/app.py` -> rota `get_racas` (usar para popular o select de raça).
  - `GET /usuarios/email/{email}` — busca usuário por email (fluxo de verificação/login leve). Implementação: `app.py`.
  - `POST /usuarios` — cria usuário (cadastro). Implementação: `app.py`.
  - `POST /cachorros` — cria cachorro associado a `user_id` e `raca_id`. Implementação: `app.py`; lógica de checagem de duplicidade retorna `409 Conflict` se o par (user_id, nome_pet) já existir.

- Integridade de dados / prevenção de duplicidade:
  - Constraint DB: UniqueConstraint em `(user_id, nome_pet)` no modelo `Cachorro`. Arquivo: `backend/database.py`.
  - Migração manual/backup: artefatos em `backend/migrations/` (backup CSVs e instruções geradas durante o processo).

- Scripts utilitários:
  - `backend/seed_db.py` — cria a pasta `instance/` (quando necessário) e popula tabela `racas` com exemplos.

- UI / Fluxos do Frontend (para demonstrar endpoints):
  - `frontend/index.html` + `frontend/script.js` implementam:
    - Verificar/cadastrar usuário via `GET /usuarios/email/{email}` e `POST /usuarios`.
    - Registrar pet via `POST /cachorros` e tratar status `409` (prefill com dados existentes).
    - Carregar raças via `GET /racas` e exibir (imagem, descrição, cards de cuidados).
    - Painel administrativo (visualizar/editar/deletar) chamando endpoints CRUD para `usuarios` e `cachorros`.

- Requisitos organizacionais:
  - `backend/README.md` criado (instruções de setup/rodar/rotas para demo).
  - `frontend/README.md` criado anteriormente com instruções de execução e pontos para a apresentação.

Notas importantes para a defesa / vídeo de 4 minutos
- Mostre o Swagger UI e o `Try it out` nas rotas: `GET /racas`, `GET /usuarios/email/{email}`, `POST /usuarios`, `POST /cachorros`.
- Demonstre o fluxo completo: seed -> verificar usuário -> criar pet -> ver cards atualizados.
- Explique a solução de integridade: UniqueConstraint no modelo e resposta 409 no endpoint de criação de pet.

Evidências de arquivo/linha (principais locais):
- `backend/app.py` — rotas e fábrica de app (ver funções `create_app`, `get_racas`, `get_user_by_email`, `create_user`, `create_cachorro`).
- `backend/database.py` — modelos `User`, `Raca`, `Cachorro` com `UniqueConstraint`.
- `backend/seed_db.py` — criação de `instance/` e inserção de raças.
- `backend/swagger.yaml` — especificação OpenAPI usada na UI.
- `frontend/script.js` — fluxos de verificação/cadastro e tratamento de duplicidade.

