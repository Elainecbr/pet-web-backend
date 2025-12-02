from pydantic import BaseModel
from typing import Optional

class ErrorSchema(BaseModel):
    """Representa uma mensagem de erro"""
    message: str
