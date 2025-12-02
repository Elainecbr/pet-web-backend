from model.base import db

class Raca(db.Model):
    """
    Modelo para a Raça do Cachorro - Representa a tabela 'raca'
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    porte = db.Column(db.String(50), nullable=True)
    grupo = db.Column(db.String(100), nullable=True)
    imagem = db.Column(db.String(100), nullable=True)
    cuidados = db.Column(db.Text, nullable=True)
    comportamento = db.Column(db.Text, nullable=True)
    racao = db.Column(db.Text, nullable=True)
    
    # Relacionamento One-to-Many: Uma raça pode ter vários cachorros
    cachorros = db.relationship('Cachorro', backref='breed', lazy=True)

    def to_dict(self):
        """Converte o objeto Raca em um dicionário para serialização JSON"""
        return {
            'id': self.id,
            'nome': self.nome,
            'porte': self.porte,
            'grupo': self.grupo,
            'imagem': self.imagem,
            'cuidados': self.cuidados,
            'comportamento': self.comportamento,
            'racao': self.racao
        }
