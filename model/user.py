from datetime import datetime
from model.base import db

class User(db.Model):
    """
    Modelo para o Usuário - Representa a tabela 'user' no banco de dados
    """
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    
    # Relacionamento One-to-Many: Um usuário pode ter vários cachorros
    cachorros = db.relationship('Cachorro', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        """Converte o objeto User em um dicionário para serialização JSON"""
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'email': self.email,
            'telefone': self.telefone,
            'data_cadastro': self.data_cadastro.isoformat() + 'Z'
        }
