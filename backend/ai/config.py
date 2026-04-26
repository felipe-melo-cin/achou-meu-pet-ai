import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class ModelConfig(Enum):
    """Modelos disponíveis no OpenRouter"""
    # Embeddings multimodal (imagem + texto)
    EMBEDDING_VISION = "nvidia/llama-nemotron-embed-vl-1b-v2:free"
    
    # Vision (análise detalhada de imagens)
    VISION_MODEL = "nvidia/llama-3.1-nemotron-70b-instruct"
    
    # Embeddings de texto (se precisar depois)
    EMBEDDING_TEXT = "nvidia/llama-nemotron-embed-vl-1b-v2:free"

class OpenRouterConfig:
    """Configurações centralizadas do OpenRouter"""
    
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    BASE_URL = "https://openrouter.ai/api/v1"
    
    # Thresholds
    MIN_SIMILARITY = 0.5  # 50% mínimo para match
    TOP_RESULTS = 5      # Top 5 matches
    
    # Timeouts
    TIMEOUT = 30
    MAX_RETRIES = 3


# Validar que a chave existe
if not OpenRouterConfig.API_KEY:
    raise ValueError("OPENROUTER_API_KEY não configurada!")