from pydantic import BaseModel
from typing import Optional

class RacaSchema(BaseModel):
    """Schema para criar uma nova raça"""
    nome: str
    porte: Optional[str] = None
    grupo: Optional[str] = None
    imagem: Optional[str] = None
    cuidados: Optional[str] = None
    comportamento: Optional[str] = None
    racao: Optional[str] = None

class RacaViewSchema(BaseModel):
    """Schema para visualizar uma raça"""
    id: int
    nome: str
    porte: Optional[str]
    grupo: Optional[str]
    imagem: Optional[str]
    cuidados: Optional[str]
    comportamento: Optional[str]
    racao: Optional[str]
