# Pet Web - Full Stack SPA 

# 🐶 Pet Web - O nosso Dogginho Care System 🐾 🐕 🐕‍🦺 🦮

Bem-vindo ao Pet Web! Este sistema permite que você cadastre suas informações e as do seu cãozinho, recebendo dicas e cuidados personalizados baseados na raça, você pode visualizar as fotos respectivas da raça. As informações após o cadastro ou login serão amostradas nos cards abaixo do formulário. Além do cadastro e visualização, é possível também modificar ou deletar as informações. 



# ⚙️ Futuramente, poderá ser escolhido: 

> <span style="color:  #9543f9;"> 🥣 Diferentes tipos de Rações,</span> <span style="color:magenta;"> 🧴 Produtos de Cuidados para o seu cão</span>, <span style="color:#70CC87;"> 🩺 Veterinários na sua região,</span> <span style="color:#8A4C57">Forum - 📖 Dog-Book - para encontrar outros tutores que queiram socializar</span> e muito mais.
> > Futuramente será possivel Monetização de Conteúdo - converter o tráfego ou o conteúdo online em receita, (marketing de afiliados, publicidade direta, conteúdo patrocinado e outras estratégias).


## Estrutura Modularizada 

O backend seguindo o padrão ensinado na disciplina Dev. Full Stack  Básico - PUC:
- ✅ **`model/`** - Modelos separados (User, Raca, Cachorro)
- ✅ **`schemas/`** - Schemas de validação Pydantic
- ✅ **Organização MVC** - Código modular e escalável

## Pet Web - Estrutura Modularizada

## 📁 Estrutura

O projeto anteriormente, eu não tinha modularizado, fiz as modificações, seguindo o padrão MVC (Model-View-Controller) ensinado na aula, 
separei as responsabilidades dos módulos do projeto, organizando o código em módulos separados:

```
backend/
├── app.py                 ✅ Principal - Rotas e endpoints da API (Controller)
├── seed_db.py             ✅ Popula o banco (NECESSÁRIO!) - Script para popular o banco
├── requirements.txt       ✅ Dependências - Dependências que devem ser instaladas (pip)
├── swagger.yaml           ✅ Documentação API
├── README.md              ✅ Instruções
├── .gitignore             ✅ Proteção - arquivos que devem ser ignorados pelo git
├── model/                 ✅ Modelos
│   ├── __init__.py         # inicializador de pacote - Inicializa DB e expõe os modelos - (Propósito: Define um diretório como um pacote Python)
│   ├── base.py             # Base do SQLAlchemy
│   ├── user.py             # Modelo User
│   ├── raca.py             # Modelo Raca
│   └── cachorro.py         # Modelo Cachorro
└── schemas/               ✅ Validação - Schemas de validação (Pydantic)
│    ├── __init__.py         # inicializador de pacote - Expõe todos os schemas
│    ├── error.py            # Schema de erro
│    ├── user.py             # Schemas de User
│    ├── raca.py             # Schemas de Raca
│    └── cachorro.py         # Schemas de Cachorro
├── Venv/                    # Após a instalação - o ambiente virtual
└── instance/                # Após a instalação - Banco de dados SQLite
    └── site.db

```

# 🐶 Projeto

Este é um projeto Full-Stack, básico, desenvolvido, como uma Single Page Application (SPA) para o "Pet Web", conforme o wireframe gráfico do projeto. O objetivo é demonstrar a integração de um backend em Python (Flask) com um frontend interativo (HTML, CSS, JavaScript), utilizando Pydantic para validação de dados e Flask-OpenAPI3 para documentação de API (Swagger UI). Seguindo os "requisitos para o MVP.pdf"

[ Link: O Wireframe gráfico simila a página](https://github-production-user-asset-6210df.s3.amazonaws.com/218513793/516668469-e8bd6e83-ac34-411a-bfeb-2472433f32b9.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20251130%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251130T233219Z&X-Amz-Expires=300&X-Amz-Signature=fbfdc7d5efcbabab3fa62a9241293bdf4112d0dcf0d9c8e100bbcc1ad81bb11b&X-Amz-SignedHeaders=host)


## Tecnologias Utilizadas
Backend em Python usando Flask e Flask-SQLAlchemy. Fornece endpoints para gerenciar usuários, raças e cachorros.

## Backend:

    Python3
    Flask: Microframework web
    Flask-OpenAPI3: Integração OpenAPI/Swagger UI com Flask e Pydantic
    Pydantic: Validação de dados (modelos para requests/responses)
    SQLAlchemy (ORM)
    SQLite3: Banco de dados relacional leve
    Flask-CORS (Cross-Origin Resource Sharing)
    
## Frontend:

    HTML5: Estrutura da página
    CSS3: Estilização responsiva
    JavaScript (ES6+): Interatividade SPA, manipulação do DOM, requisições Fetch API    
    para o backend

# Pet Web — Backend (API)

## Baixe ou clone o arquivo pet-web-backend.zip


**⚠️ IMPORTANTE:** Após clonar os dois repositórios (pet-web-backend e pet-web-frontend), renomeie as pastas para "backend" e "frontend" respectivamente, pois o backend serve tanto a API quanto o frontend na porta 5000, e o código busca a pasta frontend um nível acima do backend (../frontend). A linha de código responsável está em `app.py` linha 384:
```python
frontend_dir = os.path.abspath(os.path.join(basedir, '..', 'frontend'))
```
 
### Pré-requisitos
Certifique-se de ter o python, ou python3 e o pip (gerenciador de pacotes do Python) instalados em seu sistema. 
O SQLite3 geralmente vem pré-instalado e com o python3 no macOS.

# Backend — Projeto Pet

## Este diretório contém a API em Flask usada pelo Projeto Pet.

### Requisitos - siga os passos -
```diff
- Crie um ambiente virtual (recomendado)
- Python 3.8+ (no mac,  para usar/exucar o Python, python3 [option]  | file , ex. python3 app.py)
- Instale dependências

!IMPORTANTE:! Antes de iniciar o servidor (python3 app.py), execute:
> renomeie as pastas para "backend" e "frontend"
> python seed_db.py
> Este comando popula o banco com 24 raças de cachorro necessárias para o funcionamento do sistema.
> Siga o passo a passo abaixo

```
## Passo a Passo
### No Terminal - por exemplo do vs-code

⇥ 1. Vá ao diretorio
```
 cd backend/ (renomeie as pastas para "backend" e "frontend" apos o download ou clone)
```

⇥ 2. Criar o ambiente virtual do projeto com nome venv
```
 python3 -m venv venv
```
⇥ 3. Para ativar o ambiente virtual:
```
 source venv/bin/activate  # Mac/Linux
```
```
 venv\Scripts\activate   # Windows
```
**💡 Dica:** Para confirmar que está no ambiente correto, o terminal deve mostrar `(venv)` no início da linha.

⇥ 4. Instalar dependências:
```
 pip install -r requirements.txt
```

## Rodando localmente

⇥ 5. inicializa o banco (se necessário- se ainda não existe)
```
 python3 seed_db.py
```
    > Este comando irá:
      Criar a pasta instance/ (se não existir)
      Criar o banco site.db
      Insere 24 raças de cachorro

⇥ 6. rodar app
```
 python3 app.py
```
```
# A API ficará disponível em http://127.0.0.1:5000

```

## ⚠️ Solução de Problemas - Erro de Permissão ao Gravar Dados

Se você receber erros de JSON (, , ,) ou erro de permissão ao tentar cadastrar dados, é necessário ajustar as permissões da pasta `instance/`:

```bash
# Dar permissão de escrita na pasta instance
chmod -R 755 instance/

# Se necessário, reinicie o servidor:
# 1. Pare o servidor (Ctrl+C no terminal)
# 2. Desative e reative o ambiente virtual:
deactivate
source venv/bin/activate  # Mac/Linux

# 3. Limpe o cache Python (se necessário):
find . -type d -name __pycache__ -exec rm -rf {} +

# 4. Reinicie o servidor:
python3 app.py
```

## Banco de Dados
- O banco é um arquivo SQLite em `/instance/site.db`
- [Link da imagem](https://github.com/user-attachments/assets/8a186726-e2ee-459b-845a-6a458b49e1ec)

<img width="564" height="453" alt="image" src="https://github.com/user-attachments/assets/862b9cf7-c4e9-4509-8322-17be0c0e70ee" />

**Principais rotas para demonstração (4 exigidas pelo trabalho)**
- `GET /racas` — lista todas as raças
- `GET /usuarios/`— lista todos os usuários cadastrados. 
- `POST /usuarios` — cria usuário (ex: para cadastro)
- `POST /cachorros` — cria cachorro associado a `user_id` e `raca_id` (ex: registrar pet)

**Documentação OpenAPI/Swagger**
- Acesse a UI Swagger em: `http://127.0.0.1:5000/swagger`
- O arquivo `backend/swagger.yaml` contém a especificação completa das rotas.


