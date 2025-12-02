import os
from model.base import db

# Importando os modelos definidos
from model.user import User
from model.raca import Raca
from model.cachorro import Cachorro

def init_database(app):
    """
    Inicializa o banco de dados com a aplicação Flask.
    
    Esta função:
    - Vincula o SQLAlchemy à aplicação Flask
    - Cria o diretório 'instance' se não existir
    - Cria todas as tabelas do banco de dados
    
    Args:
        app: Instância da aplicação Flask
    """
    # Vincula o SQLAlchemy à aplicação
    db.init_app(app)
    
    # Cria a pasta 'instance' se ela não existir
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    instance_path = os.path.join(basedir, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    # Cria todas as tabelas do banco de dados
    with app.app_context():
        db.create_all()

# Exporta os elementos para serem importados facilmente
__all__ = ['db', 'User', 'Raca', 'Cachorro', 'init_database']
