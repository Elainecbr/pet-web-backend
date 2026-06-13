from datetime import datetime
from model.base import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    Modelo para o Usuário - Representa a tabela 'user' no banco de dados
    """
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False, default='')
    telefone = db.Column(db.String(20), nullable=True)

    # Relacionamento One-to-Many: Um usuário pode ter vários cachorros
    cachorros = db.relationship(
        'Cachorro',
        backref='owner',
        lazy=True,
        cascade='all, delete-orphan',
    )

    data_cadastro = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    def set_password(self, senha_plana: str):
        """Gera e armazena hash seguro da senha."""
        self.senha_hash = generate_password_hash(senha_plana)

    def check_password(self, senha_plana: str) -> bool:
        """Valida senha em texto plano contra o hash persistido."""
        if not self.senha_hash:
            return False
        return check_password_hash(self.senha_hash, senha_plana)

    def to_dict(self):
        """Converte o objeto User em um dicionário para serialização JSON"""
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'email': self.email,
            'telefone': self.telefone,
            'data_cadastro': self.data_cadastro.isoformat() + 'Z'
        }
