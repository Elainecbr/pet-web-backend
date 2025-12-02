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
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from model import db, User, Raca, Cachorro, init_database
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime

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

    # Nota: a rota que serve o frontend (catch-all) foi movida para o final
    # da função `create_app()` para evitar sobrescrever as rotas da API.


    # --- Rotas da API ---

    # Rota GET para buscar todas as raças de cachorro
    @app.route('/racas', methods=['GET'])
    def get_racas():
        # Consulta todas as raças no banco de dados
        racas = Raca.query.all()
        # Converte a lista de objetos Raca para uma lista de dicionários e retorna como JSON
        return jsonify([raca.to_dict() for raca in racas])

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
                "nome_completo": "Nome do usuário",
                "email": "usuario@example.com",
                "telefone": "(XX) XXXXX-XXXX"  # opcional
            }

        Respostas:
            201: objeto do usuário criado (JSON)
            400: dados incompletos
            409: e-mail já cadastrado
        """

        data = request.get_json()  # Pega os dados JSON enviados no corpo da requisição

        # Validação básica: verifica se os campos 'nome_completo' e 'email' estão presentes
        if not data or not all(key in data for key in ['nome_completo', 'email']):
            return jsonify({"message": "Dados incompletos para cadastro de usuário."}), 400 # 400 (Bad Request)

        # Verifica se o email já existe no banco de dados para evitar duplicatas
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"message": "Este e-mail já está cadastrado."}), 409 # 409 (Conflict)

        # Cria um novo objeto User com os dados recebidos
        new_user = User(
            nome_completo=data['nome_completo'],
            email=data['email'],
            telefone=data.get('telefone') # .get() permite que 'telefone' seja opcional
        )
        db.session.add(new_user) # Adiciona o novo usuário à sessão do banco
        db.session.commit() # Salva as mudanças permanentemente
        return jsonify(new_user.to_dict()), 201 # Retorna o usuário criado e 201 (Created)

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
        data = request.get_json()
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

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404
        data = request.get_json() or {}
        user.nome_completo = data.get('nome_completo', user.nome_completo)
        user.email = data.get('email', user.email)
        user.telefone = data.get('telefone', user.telefone)
        db.session.commit()
        return jsonify(user.to_dict())

    # Rota GET para buscar todos os usuários (útil para debug ou admin, mas não essencial no frontend MVP)
    @app.route('/usuarios', methods=['GET'])
    def get_all_users():
        """Retorna todos os usuários cadastrados (útil para administração).

        Uso: GET /usuarios
        """

        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

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
    
    # Inicia o servidor Flask. 'debug=True' é útil em desenvolvimento.
    # Quando iniciamos o processo em background (nohup) o reloader pode tentar
    # acessar descriptors de terminal e causar erros (termios). Desativamos o
    # reloader para execução em background local segura.
    app.run(debug=True, use_reloader=False, port=5000)
