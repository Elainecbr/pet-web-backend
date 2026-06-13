# backend/app.py
"""
Módulo principal do backend Flask para o projeto Pet Web.

Este arquivo contém a fábrica de aplicação `create_app()` que:
- configura a conexão com o banco SQLite;
- inicializa extensões (SQLAlchemy, CORS);
- registra o Swagger UI para documentação;
- define as rotas REST usadas pelo frontend (usuários, raças e cachorros);
- serve os arquivos estáticos do frontend como uma SPA (catch-all).

Você pode executar este arquivo diretamente para iniciar o servidor
em modo desenvolvimento: `python app.py` (ele cria o DB em `instance/site.db`).
"""

import os
import requests as http_requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from model import db, User, Raca, Cachorro, init_database
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
from sqlalchemy import inspect, text

# Chave da TheDogAPI lida do ambiente — nunca hardcoded no código.
DOG_API_KEY = os.getenv('DOG_API_KEY', '')
DOG_API_BREEDS_URL = 'https://api.thedogapi.com/v1/breeds'

# --- Configuração do Flask App e SQLAlchemy ---
def create_app():
    """Cria e configura a aplicação Flask.

    Retorna a instância do app pronta para ser usada tanto pelo servidor
    quanto por scripts (ex: `seed_db.py`). Separar a criação da app em
    uma fábrica facilita testes e execução em diferentes contextos.
    """

    app = Flask(__name__) # Cria a instância do aplicativo Flask
    
    # Configura o URI do banco de dados SQLite usando caminho absoluto.
    # Assim evitamos problemas quando o script for executado a partir de outro diretório.
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'site.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    
    # Desativa um alerta do SQLAlchemy que não é necessário para o nosso caso, economizando recursos.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa o SQLAlchemy e cria as tabelas do banco de dados
    init_database(app)

    # Migração leve para ambientes já existentes: adiciona coluna de senha
    # se o banco tiver sido criado antes deste requisito de autenticação.
    with app.app_context():
        user_columns = [c['name'] for c in inspect(db.engine).get_columns('user')]
        if 'senha_hash' not in user_columns:
            db.session.execute(
                text("ALTER TABLE user ADD COLUMN senha_hash VARCHAR(255) NOT NULL DEFAULT ''")
            )
            db.session.commit()

    # Habilita o CORS (Cross-Origin Resource Sharing) para todas as rotas.
    # Isso é essencial para permitir que o Frontend (rodando em um domínio/porta diferente)
    # se comunique com o Backend sem bloqueios de segurança do navegador.
    CORS(app)

    # --- Configuração do Swagger UI ---
    SWAGGER_URL = '/swagger' # URL onde a documentação Swagger estará disponível (ex: http://localhost:5000/swagger)
    API_URL = '/swagger.yaml' # Caminho para o nosso arquivo YAML de documentação

    # Cria um Blueprint (um módulo de rotas) para o Swagger UI.
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Pet Web API" # Nome que aparecerá na interface do Swagger
        }
    )
    # Registra o Blueprint do Swagger UI no nosso aplicativo Flask.
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Rota para servir arquivos estáticos (como o swagger.yaml) que não estão na pasta 'static' padrão do Flask.
    # Serve arquivos a partir do diretório do backend (onde este app.py vive).
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(basedir, filename)

    # Rota dedicada para servir o arquivo OpenAPI/Swagger diretamente.
    @app.route('/swagger.yaml')
    def swagger_yaml():
        return send_from_directory(basedir, 'swagger.yaml')

    def _get_request_user_id():
        """Lê o usuário autenticado via header X-User-Id.

        Retorna:
            int: id do usuário autenticado
            None: header ausente
            -1: header inválido
        """

        raw = (request.headers.get('X-User-Id') or '').strip()
        if not raw:
            return None
        try:
            user_id = int(raw)
            return user_id if user_id > 0 else -1
        except ValueError:
            return -1

    def _require_self(target_user_id):
        """Garante que o usuário autenticado só acesse o próprio recurso."""

        requester_user_id = _get_request_user_id()
        if requester_user_id is None:
            return jsonify({"message": "Autenticação ausente. Faça login novamente."}), 401
        if requester_user_id == -1:
            return jsonify({"message": "Header X-User-Id inválido."}), 400
        if requester_user_id != target_user_id:
            return jsonify({"message": "Acesso negado: você só pode acessar seus próprios dados."}), 403
        return None

    # Nota: a rota que serve o frontend (catch-all) foi movida para o final
    # da função `create_app()` para evitar sobrescrever as rotas da API.


    # --- Rotas da API ---

    # Rota GET para buscar todas as raças de cachorro
    # Se DOG_API_KEY estiver definida, enriquece cada raça com a foto real da TheDogAPI.
    @app.route('/racas', methods=['GET'])
    def get_racas():
        racas = Raca.query.all()
        resultado = [r.to_dict() for r in racas]

        if DOG_API_KEY:
            try:
                resp = http_requests.get(
                    DOG_API_BREEDS_URL,
                    headers={'x-api-key': DOG_API_KEY},
                    timeout=5
                )
                if resp.ok:
                    dog_breeds = resp.json()  # lista completa de raças da TheDogAPI
                    # Cria mapa nome_normalizado -> url_imagem
                    img_map = {}
                    for b in dog_breeds:
                        nome_norm = b.get('name', '').lower()
                        img = b.get('image', {}).get('url')
                        if img:
                            img_map[nome_norm] = img

                    # Substitui a imagem local pela foto real quando existir
                    for raca_dict in resultado:
                        nome_norm = raca_dict['nome'].lower()
                        # Tenta correspondência exata ou parcial
                        img_url = img_map.get(nome_norm)
                        if not img_url:
                            # Busca parcial: verifica se algum nome da API contém o nome local
                            for api_nome, api_img in img_map.items():
                                if nome_norm in api_nome or api_nome in nome_norm:
                                    img_url = api_img
                                    break
                        if img_url:
                            raca_dict['imagem_api'] = img_url
            except Exception:
                pass  # Se a API externa falhar, usa apenas os dados do banco local

        return jsonify(resultado)

    # Rota GET para buscar uma raça específica pelo nome
    # O nome da raça é passado como parte da URL (ex: /racas/Bulldog-Frances)
    @app.route('/racas/<string:nome_raca>', methods=['GET'])
    def get_raca_by_name(nome_raca):
        # Converte o nome da raça recebido na URL para um formato que corresponda ao banco de dados.
        # Ex: "bulldog-frances" -> "Bulldog Frances" ou "labrador-retriever" -> "Labrador Retriever"
        # .replace('-', ' ') substitui hífens por espaços.
        # .title() capitaliza a primeira letra de cada palavra (para nomes compostos como 'Bulldog Frances').
        formatted_name = nome_raca.replace('-', ' ').title()
        raca = Raca.query.filter_by(nome=formatted_name).first() # Busca a raça pelo nome
        if raca:
            return jsonify(raca.to_dict()) # Retorna os dados da raça como JSON
        return jsonify({"message": "Raça não encontrada."}), 404 # Se não encontrar, retorna 404 (Not Found)

    # Rota POST para cadastrar um novo usuário
    @app.route('/usuarios', methods=['POST'])
    def create_user():
        """Cria um novo usuário.

        Payload esperado (JSON):
            {
                "nome_completo": "Nome de usuário",
                "email": "usuario@example.com",
                "senha": "senha_em_texto_plano",
                "telefone": "(XX) XXXXX-XXXX"  # opcional
            }

        Respostas:
            201: objeto do usuário criado (JSON)
            400: dados incompletos
            409: e-mail já cadastrado
        """

        data = request.get_json()  # Pega os dados JSON enviados no corpo da requisição

        nome = (data or {}).get('nome_completo', '').strip()
        email = (data or {}).get('email', '').strip().lower()
        senha = (data or {}).get('senha', '').strip()

        # Validação básica: campos obrigatórios para autenticação
        if not nome or not email or not senha:
            return jsonify({"message": "Dados incompletos para cadastro de usuário."}), 400 # 400 (Bad Request)

        # Verifica se o email já existe no banco de dados para evitar duplicatas
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Este e-mail já está cadastrado."}), 409 # 409 (Conflict)

        # Cria um novo objeto User com os dados recebidos
        new_user = User(
            nome_completo=nome,
            email=email,
            telefone=data.get('telefone') # .get() permite que 'telefone' seja opcional
        )
        new_user.set_password(senha)
        db.session.add(new_user) # Adiciona o novo usuário à sessão do banco
        db.session.commit() # Salva as mudanças permanentemente
        return jsonify(new_user.to_dict()), 201 # Retorna o usuário criado e 201 (Created)

    # Rota POST para login simplificado (nome + e-mail + senha)
    @app.route('/auth/login', methods=['POST'])
    def auth_login():
        """Autentica usuário usando nome de usuário, e-mail e senha.

        Payload esperado (JSON):
            {
                "nome_completo": "Nome de usuário",
                "email": "usuario@example.com",
                "senha": "senha_em_texto_plano"
            }

        Respostas:
            200: usuário autenticado
            400: dados incompletos
            401: credenciais inválidas
            404: usuário não encontrado
        """

        data = request.get_json() or {}
        nome = data.get('nome_completo', '').strip()
        email = data.get('email', '').strip().lower()
        senha = data.get('senha', '').strip()

        if not nome or not email or not senha:
            return jsonify({"message": "Informe nome de usuário, e-mail e senha."}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404

        if user.nome_completo.strip().lower() != nome.lower():
            return jsonify({"message": "Nome de usuário não confere com o e-mail informado."}), 401

        # Compatibilidade com usuários legados sem senha cadastrada.
        if not user.senha_hash:
            user.set_password(senha)
            db.session.commit()
            return jsonify(user.to_dict()), 200

        if not user.check_password(senha):
            return jsonify({"message": "Senha incorreta."}), 401

        return jsonify(user.to_dict()), 200

    # Rota GET para buscar um usuário específico pelo e-mail
    @app.route('/usuarios/email/<string:email>', methods=['GET'])
    def get_user_by_email(email):
        """Retorna um usuário pelo e-mail.

        Uso: GET /usuarios/email/{email}
        Retorna 200 com o objeto `User` ou 404 se não existir.
        """

        user = User.query.filter_by(email=email).first() # Busca o usuário pelo email
        if user:
            # Retorna o usuário. Opcionalmente, poderíamos incluir os cachorros associados aqui.
            return jsonify(user.to_dict()) 
        return jsonify({"message": "Usuário não encontrado."}), 404

    # Rota POST para cadastrar um novo cachorro
    @app.route('/cachorros', methods=['POST'])
    def create_cachorro():
        """Cadastra um novo cachorro associado a um usuário e a uma raça.

        Payload esperado (JSON):
            {
                "nome_pet": "Rex",
                "user_id": 1,
                "raca_id": 2,
                "idade": 3,            # opcional
                "peso": 12.5,          # opcional
                "info_extra": "Alergia a ..."  # opcional
            }

        Respostas:
            201: cachorro criado (inclui dados da raça)
            400: dados incompletos
            404: usuário ou raça não encontrados
            409: cachorro com mesmo nome já cadastrado para esse usuário
        """

        data = request.get_json()  # Pega os dados JSON do cachorro

        # Validação: verifica se os campos obrigatórios estão presentes
        if not data or not all(key in data for key in ['nome_pet', 'user_id', 'raca_id']):
            return jsonify({"message": "Dados incompletos para cadastro de cachorro."}), 400

        auth_error = _require_self(data['user_id'])
        if auth_error:
            return auth_error

        # Verifica se o usuário e a raça (pelos IDs) existem no banco de dados
        user = User.query.get(data['user_id']) # Busca o usuário pelo ID
        raca = Raca.query.get(data['raca_id']) # Busca a raça pelo ID

        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404
        if not raca:
            return jsonify({"message": "Raça não encontrada."}), 404

        # Verifica duplicidade: mesmo user_id + nome_pet não deve existir
        existing = Cachorro.query.filter_by(user_id=data['user_id'], nome_pet=data['nome_pet']).first()
        if existing:
            # Retorna 409 Conflict com os dados existentes
            return jsonify({
                'message': 'Cachorro já registrado para este usuário.',
                'cachorro': existing.to_dict(include_breed=True)
            }), 409

        # Cria um novo objeto Cachorro
        new_cachorro = Cachorro(
            nome_pet=data['nome_pet'],
            idade=data.get('idade'),
            peso=data.get('peso'),
            info_extra=data.get('info_extra'),
            user_id=data['user_id'], # Associa o cachorro ao usuário
            raca_id=data['raca_id'] # Associa o cachorro à raça
        )
        db.session.add(new_cachorro)
        db.session.commit()
        return jsonify(new_cachorro.to_dict(include_breed=True)), 201

    # Rota GET para buscar todos os cachorros de um usuário específico
    # O ID do usuário é passado como parte da URL (ex: /usuarios/1/cachorros)
    @app.route('/usuarios/<int:user_id>/cachorros', methods=['GET'])
    def get_cachorros_by_user(user_id):
        """Retorna todos os cachorros pertencentes a um usuário.

        Uso: GET /usuarios/{user_id}/cachorros
        Responde 200 com uma lista de `CachorroWithBreed` ou 404 se o usuário não existir.
        """

        auth_error = _require_self(user_id)
        if auth_error:
            return auth_error

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404
        
        # Busca todos os cachorros associados a este user_id
        cachorros = Cachorro.query.filter_by(user_id=user_id).all()
        # Retorna a lista de cachorros, incluindo os dados da raça para cada um
        return jsonify([c.to_dict(include_breed=True) for c in cachorros])

    # Rota GET para buscar um cachorro específico de um usuário pelo nome do pet
    @app.route('/usuarios/<int:user_id>/cachorros/<string:nome_pet>', methods=['GET'])
    def get_cachorro_by_user_and_name(user_id, nome_pet):
        """Busca um cachorro específico de um usuário pelo nome do pet.

        Uso: GET /usuarios/{user_id}/cachorros/{nome_pet}
        Nota: o `nome_pet` deve ser exatamente igual ao cadastrado (case-sensitive).
        """

        auth_error = _require_self(user_id)
        if auth_error:
            return auth_error

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404
        # Procura pelo nome exato (não formatamos aqui, assumimos nome_pet enviado corretamente)
        cachorro = Cachorro.query.filter_by(user_id=user_id, nome_pet=nome_pet).first()
        if cachorro:
            return jsonify(cachorro.to_dict(include_breed=True))
        return jsonify({"message": "Cachorro não encontrado."}), 404

    # Rota DELETE para remover um cachorro (exemplo de exclusão)
    @app.route('/cachorros/<int:cachorro_id>', methods=['DELETE'])
    def delete_cachorro(cachorro_id):
        """Exclui um cachorro pelo seu ID.

        Uso: DELETE /cachorros/{cachorro_id}
        Responde 200 em sucesso ou 404 se não encontrado.
        """

        cachorro = Cachorro.query.get(cachorro_id)
        if not cachorro:
            return jsonify({"message": "Cachorro não encontrado."}), 404

        auth_error = _require_self(cachorro.user_id)
        if auth_error:
            return auth_error
        
        db.session.delete(cachorro) # Remove o cachorro da sessão
        db.session.commit() # Salva a exclusão
        return jsonify({"message": "Cachorro removido com sucesso."}), 200 # 200 (OK)

    # Rota GET para buscar um cachorro por ID
    @app.route('/cachorros/<int:cachorro_id>', methods=['GET'])
    def get_cachorro_by_id(cachorro_id):
        """Retorna um cachorro por ID incluindo os dados da raça.

        Uso: GET /cachorros/{cachorro_id}
        """

        cachorro = Cachorro.query.get(cachorro_id)
        if not cachorro:
            return jsonify({"message": "Cachorro não encontrado."}), 404

        auth_error = _require_self(cachorro.user_id)
        if auth_error:
            return auth_error
        return jsonify(cachorro.to_dict(include_breed=True))

    # Rota PUT para atualizar um cachorro por ID
    @app.route('/cachorros/<int:cachorro_id>', methods=['PUT'])
    def update_cachorro(cachorro_id):
        """Atualiza os campos de um cachorro existente.

        Payload aceito (parcialmente):
            {
                "nome_pet": "Novo Nome",
                "idade": 4,
                "peso": 13.2,
                "info_extra": "...",
                "raca_id": 3,
                "user_id": 2
            }

        Verificamos a existência da `raca_id` e `user_id` caso sejam fornecidos.
        """

        cachorro = Cachorro.query.get(cachorro_id)
        if not cachorro:
            return jsonify({"message": "Cachorro não encontrado."}), 404

        auth_error = _require_self(cachorro.user_id)
        if auth_error:
            return auth_error

        data = request.get_json() or {}
        # Atualiza campos se fornecidos
        cachorro.nome_pet = data.get('nome_pet', cachorro.nome_pet)
        cachorro.idade = data.get('idade', cachorro.idade)
        cachorro.peso = data.get('peso', cachorro.peso)
        cachorro.info_extra = data.get('info_extra', cachorro.info_extra)
        # Se estiver alterando a raça ou user_id, verificar existência
        if 'raca_id' in data:
            if not Raca.query.get(data['raca_id']):
                return jsonify({"message": "Raça não encontrada."}), 404
            cachorro.raca_id = data['raca_id']
        if 'user_id' in data:
            if data['user_id'] != cachorro.user_id:
                return jsonify({"message": "Ação não permitida: não é possível transferir o pet para outro usuário."}), 403
            if not User.query.get(data['user_id']):
                return jsonify({"message": "Usuário não encontrado."}), 404
            cachorro.user_id = data['user_id']
        db.session.commit()
        return jsonify(cachorro.to_dict(include_breed=True))

    # Rota GET para buscar um usuário por ID
    @app.route('/usuarios/<int:user_id>', methods=['GET'])
    def get_user_by_id(user_id):
        """Retorna um usuário pelo ID.

        Uso: GET /usuarios/{user_id}
        """

        auth_error = _require_self(user_id)
        if auth_error:
            return auth_error

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404
        return jsonify(user.to_dict())

    # Rota DELETE para remover um usuário
    @app.route('/usuarios/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        """Remove um usuário e todos os cachorros associados (cascade).

        Uso: DELETE /usuarios/{user_id}
        """

        auth_error = _require_self(user_id)
        if auth_error:
            return auth_error

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404
        # Remove usuário e seus cachorros via cascade
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário removido com sucesso."}), 200

    # Rota PUT para atualizar um usuário por ID
    @app.route('/usuarios/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        """Atualiza os dados de um usuário.

        Payload aceito (parcial):
            { "nome_completo": "Novo nome", "email": "novo@example.com", "telefone": "..." }
        """

        auth_error = _require_self(user_id)
        if auth_error:
            return auth_error

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404
        data = request.get_json() or {}
        user.nome_completo = data.get('nome_completo', user.nome_completo)
        if 'email' in data:
            novo_email = (data.get('email') or '').strip().lower()
            if novo_email and novo_email != user.email:
                existing_user = User.query.filter_by(email=novo_email).first()
                if existing_user and existing_user.id != user.id:
                    return jsonify({"message": "Este e-mail já está cadastrado."}), 409
                user.email = novo_email
        user.telefone = data.get('telefone', user.telefone)
        nova_senha = (data.get('senha') or '').strip()
        if nova_senha:
            user.set_password(nova_senha)
        db.session.commit()
        return jsonify(user.to_dict())

    # ---------------------------------------------------------------------------
    # Rota POST /saude/sintomas
    # Recebe sintomas e opcionalmente uma raca_id, e retorna recomendações de
    # cuidados e alertas baseados nas informações da raça cadastrada no banco.
    # ---------------------------------------------------------------------------
    @app.route('/saude/sintomas', methods=['POST'])
    def consulta_saude():
        """Consulta de saúde com base em sintomas descritos pelo tutor.

        Payload esperado (JSON):
            {
                "sintomas": "letargia, sem apetite, vômito",
                "raca_id": 3          # opcional
            }

        Resposta 200:
            {
                "alerta": "⚠️ Sintomas como vômito e letargia podem indicar...",
                "recomendacoes": ["Leve ao veterinário em até 24h", ...],
                "cuidados_da_raca": "...",   # se raca_id informado
                "raca": "Labrador Retriever"  # se raca_id informado
            }
        """
        data = request.get_json() or {}
        sintomas_raw = data.get('sintomas', '').strip().lower()

        if not sintomas_raw:
            return jsonify({"message": "Informe os sintomas do seu pet."}), 400

        # ------------------------------------------------------------------
        # Tabela de triagem por palavras-chave nos sintomas
        # Cada entrada: (palavras-chave, nível de urgência, recomendações)
        # ------------------------------------------------------------------
        TRIAGEM = [
            (
                ['convuls', 'desmaiou', 'desmaio', 'paralisia', 'paralisi', 'inconsci'],
                'urgente',
                [
                    '🚨 URGENTE: Leve imediatamente ao veterinário ou emergência animal.',
                    'Não tente forçar o animal a se mover.',
                    'Mantenha-o aquecido e em local seguro durante o transporte.',
                ]
            ),
            (
                ['vomit', 'vômit', 'diarr', 'sangue', 'fezes com sangue', 'urina com sangue'],
                'atenção',
                [
                    '⚠️ Leve ao veterinário em até 24 horas.',
                    'Ofereça água limpa em pequenas quantidades para evitar desidratação.',
                    'Evite alimentá-lo até a consulta para não agravar o quadro.',
                    'Observe se os sintomas pioram — se sim, vá imediatamente.',
                ]
            ),
            (
                ['letargi', 'apático', 'apatia', 'sem apetit', 'não quer comer', 'nao quer comer'],
                'observação',
                [
                    '👀 Monitore por 24–48 horas.',
                    'Verifique se há febre tocando o focinho (seco e quente pode indicar febre).',
                    'Ofereça água fresca e alimento palatável.',
                    'Se persistir por mais de 48 horas, consulte um veterinário.',
                ]
            ),
            (
                ['coçando', 'cocando', 'coça', 'coça muito', 'alergi', 'vermelhidão', 'vermelhidao', 'mancha'],
                'observação',
                [
                    '👀 Pode ser alergia alimentar, ambiental ou parasita externo (pulga, carrapato).',
                    'Verifique a pelagem por parasitas.',
                    'Evite trocar a ração de forma abrupta.',
                    'Consulte um veterinário se a coceira for intensa ou houver feridas.',
                ]
            ),
            (
                ['tosse', 'espirro', 'espirrando', 'coriza', 'nariz escorrendo', 'respiração difícil', 'respiracao dificil'],
                'atenção',
                [
                    '⚠️ Pode indicar infecção respiratória ou traqueobronquite (tosse do canil).',
                    'Mantenha o animal em local arejado e aquecido.',
                    'Evite passeios em locais com outros cães até a consulta.',
                    'Leve ao veterinário se a tosse durar mais de 2 dias ou houver dificuldade respiratória.',
                ]
            ),
            (
                ['mancando', 'manca', 'dor na pata', 'pata inchada', 'não apoia', 'nao apoia'],
                'observação',
                [
                    '👀 Inspecione a pata por espinhos, cortes ou inchaço.',
                    'Evite caminhadas longas até identificar a causa.',
                    'Se houver inchaço visível ou dor intensa, consulte um veterinário.',
                ]
            ),
            (
                ['olho', 'olhos', 'secreção ocular', 'secrecao ocular', 'olho vermelho', 'lacrimejando'],
                'observação',
                [
                    '👀 Pode ser conjuntivite ou corpo estranho no olho.',
                    'Não aplique colírio humano sem orientação veterinária.',
                    'Leve ao veterinário se a secreção for amarelada ou o olho estiver fechado.',
                ]
            ),
        ]

        recomendacoes = []
        nivel = 'geral'
        alerta = ''

        for palavras, nivel_triagem, recs in TRIAGEM:
            if any(p in sintomas_raw for p in palavras):
                recomendacoes = recs
                nivel = nivel_triagem
                break

        # Recomendação genérica se nenhuma palavra-chave bater
        if not recomendacoes:
            recomendacoes = [
                'Observe o comportamento do animal nas próximas 24 horas.',
                'Certifique-se de que ele está bem hidratado.',
                'Em caso de dúvida, sempre consulte um veterinário.',
            ]
            alerta = 'ℹ️ Não identificamos sintomas críticos nas informações fornecidas. Monitore seu pet.'
        else:
            if nivel == 'urgente':
                alerta = '🚨 URGENTE — Procure atendimento veterinário imediatamente!'
            elif nivel == 'atenção':
                alerta = '⚠️ Atenção — Recomendamos consulta veterinária em breve.'
            else:
                alerta = '👀 Monitorar — Observe o pet e consulte o veterinário se piorar.'

        resposta = {
            'alerta': alerta,
            'nivel': nivel,
            'recomendacoes': recomendacoes,
            'sintomas_recebidos': sintomas_raw,
        }

        # Se raca_id informado, enriquece a resposta com os cuidados da raça
        raca_id = data.get('raca_id')
        if raca_id:
            raca = Raca.query.get(raca_id)
            if raca:
                resposta['raca'] = raca.nome
                resposta['cuidados_da_raca'] = raca.cuidados or 'Nenhum cuidado específico cadastrado para esta raça.'
                resposta['comportamento'] = raca.comportamento or ''

        return jsonify(resposta), 200

    # Rota GET para buscar todos os usuários (útil para debug ou admin, mas não essencial no frontend MVP)
    @app.route('/usuarios', methods=['GET'])
    def get_all_users():
        """Retorna todos os usuários cadastrados (útil para administração).

        Uso: GET /usuarios
        """

        requester_user_id = _get_request_user_id()
        if requester_user_id is None:
            return jsonify({"message": "Autenticação ausente. Faça login novamente."}), 401
        if requester_user_id == -1:
            return jsonify({"message": "Header X-User-Id inválido."}), 400

        user = User.query.get(requester_user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404

        return jsonify([user.to_dict()])

    # --- Servir Frontend estático (catch-all) ---
    # Define o diretório do frontend (pasta `frontend` no nível do projeto)
    frontend_dir = os.path.abspath(os.path.join(basedir, '..', 'frontend'))

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        # Se o arquivo pedido existir na pasta frontend (ex: CSS/JS/imagens), retorna ele
        target = os.path.join(frontend_dir, path)
        if path and os.path.exists(target):
            return send_from_directory(frontend_dir, path)
        # Caso contrário, retorna o index.html (SPA)
        return send_from_directory(frontend_dir, 'index.html')

    return app # Retorna a instância do aplicativo Flask configurada

# Este bloco só é executado quando você roda 'python app.py' diretamente
if __name__ == '__main__':
    # Execução direta do script (útil em desenvolvimento/local):
    app = create_app() # Cria a instância do aplicativo (já inicializa o banco via init_database)
    
    # host='0.0.0.0' é obrigatório no Render para que o serviço seja detectado.
    # PORT é injetado pelo Render; cai para 5000 em desenvolvimento local.
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
