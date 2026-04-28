from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PetBase(BaseModel):
    id: str
    status: str  # 'perdido' | 'encontrado'
    
    nome: Optional[str] = "Desconhecido"
    
    foto_caminho: str
    
    localizacao_cidade: Optional[str] = None
    
    descricao_json: Optional[dict] = Field(
        default=None, 
        description="Dados detalhados extraídos pela IA"
    )
    
    pet_vector: Optional[List[float]] = None
    
    criado_em: datetime

    class Config:
        from_attributes = True

class ResultadoIA(BaseModel):
    descricao: str
    raca: Optional[str]
    cor: Optional[str]
    vetor: List[float]  

class FiltroBusca(BaseModel):
    status: str
    cidade: Optional[str]
    raca: Optional[str]