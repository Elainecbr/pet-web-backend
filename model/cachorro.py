from datetime import datetime
from model.base import db

class Cachorro(db.Model):
    """
    Modelo para o Cachorro - Representa a tabela 'cachorro'
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # Constraint para evitar que o mesmo usuário registre dois cães com o mesmo nome
    __table_args__ = (db.UniqueConstraint('user_id', 'nome_pet', name='uix_user_pet'),)
    
    nome_pet = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=True)
    peso = db.Column(db.Float, nullable=True)
    info_extra = db.Column(db.Text, nullable=True)
    data_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Chaves estrangeiras para relacionar com User e Raca
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    raca_id = db.Column(db.Integer, db.ForeignKey('raca.id'), nullable=False)

    def to_dict(self, include_owner=False, include_breed=False):
        """
        Converte o objeto Cachorro em um dicionário para serialização JSON
        
        Args:
            include_owner: Se True, inclui os dados completos do usuário proprietário
            include_breed: Se True, inclui os dados completos da raça
        """
        data = {
            'id': self.id,
            'nome_pet': self.nome_pet,
            'idade': self.idade,
            'peso': self.peso,
            'info_extra': self.info_extra,
            'data_registro': self.data_registro.isoformat() + 'Z',
            'user_id': self.user_id,
            'raca_id': self.raca_id
        }
        
        if include_owner and self.owner:
            data['owner'] = self.owner.to_dict()
            
        if include_breed and self.breed:
            data['breed'] = self.breed.to_dict()
            
        return data
