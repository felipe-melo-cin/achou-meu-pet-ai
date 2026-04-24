# api/models.py
from pydantic import BaseModel
from typing import Optional, List

class ResultadoIA(BaseModel):
    descricao: str
    raca: Optional[str]
    cor: Optional[str]
    vetor: List[float]  