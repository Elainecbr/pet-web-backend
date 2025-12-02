from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    """Schema para criar um novo usuário"""
    nome_completo: str
    email: str
    telefone: Optional[str] = None

class UserViewSchema(BaseModel):
    """Schema para visualizar um usuário"""
    id: int
    nome_completo: str
    email: str
    telefone: Optional[str]
    data_cadastro: str
