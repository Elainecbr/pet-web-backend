from pydantic import BaseModel
from typing import Optional

class CachorroSchema(BaseModel):
    """Schema para criar um novo cachorro"""
    nome_pet: str
    user_id: int
    raca_id: int
    idade: Optional[int] = None
    peso: Optional[float] = None
    info_extra: Optional[str] = None

class CachorroViewSchema(BaseModel):
    """Schema para visualizar um cachorro"""
    id: int
    nome_pet: str
    user_id: int
    raca_id: int
    idade: Optional[int]
    peso: Optional[float]
    info_extra: Optional[str]
    data_registro: str
