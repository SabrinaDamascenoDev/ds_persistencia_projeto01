from typing import Optional
from pydantic import BaseModel, Field


class LivroSchema(BaseModel):
    titulo: str
    autor: str
    quantidade_paginas: int
    editora: str
    genero: str
    deleted: bool = Field(default=False)

class LivroUpdateSchema(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    quantidade_paginas: Optional[int] = None
    editora: Optional[str] = None
    genero: Optional[str] = None
