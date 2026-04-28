import os
from dotenv import load_dotenv
from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional

load_dotenv()

# ============================================================================
# ENUMS DE CONFIGURAÇÃO
# ============================================================================

class APIProvider(Enum):
    """Provedores de API disponíveis"""
    OPENROUTER = "openrouter"
    GEMINI = "gemini"

class ModelConfig(Enum):
    """Modelos disponíveis por provedor"""
    
    # OpenRouter Models (Exemplos comuns de visão)
    OPENROUTER_VISION = "baidu/qianfan-ocr-fast:free" # Ou "anthropic/claude-3-haiku"
    
    # Gemini Models 
    GEMINI_VISION = "gemini-2.0-flash"

# ============================================================================
# CLASSE BASE ABSTRATA PARA API CONFIG
# ============================================================================

class BaseAPIConfig(ABC):
    """Classe base para configurações de API"""
    
    @abstractmethod
    def validate(self) -> bool:
        """Valida se a configuração está correta"""
        pass
    
    @abstractmethod
    def get_client(self):
        """Retorna o cliente da API"""
        pass


# ============================================================================
# CONFIGURAÇÃO DO OPENROUTER
# ============================================================================

class OpenRouterConfig(BaseAPIConfig):
    """Configurações centralizadas do OpenRouter"""
    
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    BASE_URL = "https://openrouter.ai/api/v1"
    PROVIDER = APIProvider.OPENROUTER
    
    # Timeouts
    TIMEOUT = 30
    MAX_RETRIES = 3
    
    @classmethod
    def validate(cls) -> bool:
        """Valida configuração do OpenRouter"""
        if not cls.API_KEY:
            # Não lança erro imediatamente para permitir rodar outros testes
            return False
        return True
    
    @classmethod
    def get_client(cls):
        """Retorna cliente OpenRouter (via OpenAI SDK compatível)"""
        if not cls.validate():
            raise ValueError("OPENROUTER_API_KEY não configurada!")
        
        # OpenRouter é compatível com o cliente OpenAI
        from openai import OpenAI
        return OpenAI(
            base_url=cls.BASE_URL,
            api_key=cls.API_KEY,
        )


# ============================================================================
# CONFIGURAÇÃO DO GEMINI
# ============================================================================

class GeminiConfig(BaseAPIConfig):
    """Configurações centralizadas do Gemini"""
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    PROVIDER = APIProvider.GEMINI
    
    # Configurações padrão
    TIMEOUT = 30
    MAX_RETRIES = 3
    
    @classmethod
    def validate(cls) -> bool:
        """Valida configuração do Gemini"""
        if not cls.API_KEY:
            return False
        return True
    
    @classmethod
    def get_client(cls):
        """Retorna cliente Gemini"""
        if not cls.validate():
            raise ValueError("GEMINI_API_KEY não configurada!")
        import google.generativeai as genai
        genai.configure(api_key=cls.API_KEY)
        return genai


# ============================================================================
# FÁBRICA DE CONFIGURAÇÃO (Factory Pattern)
# ============================================================================

class APIConfigFactory:
    """Factory para obter a configuração correta da API"""
    
    _configs = {
        APIProvider.OPENROUTER: OpenRouterConfig,
        APIProvider.GEMINI: GeminiConfig,
    }
    
    @classmethod
    def get_config(cls, provider: APIProvider) -> BaseAPIConfig:
        """
        Obtém a configuração para um provedor específico
        """
        if provider not in cls._configs:
            raise ValueError(f"Provedor '{provider}' não suportado!")
        return cls._configs[provider]


# ============================================================================
# CONFIGURAÇÃO GERAL DO PROJETO
# ============================================================================

class ProjectConfig:
    """Configurações gerais do projeto"""
    
    # Default providers por tipo de modelo
    DEFAULT_VISION_PROVIDER = APIProvider.GEMINI
    
    # Ativar logs
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    @staticmethod
    def print_status():
        """Exibe status das configurações"""
        print("=" * 60)
        print("STATUS DE CONFIGURAÇÃO DO PROJETO")
        print("=" * 60)
        
        status_or = "✓" if OpenRouterConfig.validate() else "✗"
        print(f"{status_or} OpenRouter API: {'Configurada' if OpenRouterConfig.validate() else 'Não encontrada'}")
        
        status_gem = "✓" if GeminiConfig.validate() else "✗"
        print(f"{status_gem} Gemini API: {'Configurada' if GeminiConfig.validate() else 'Não encontrada'}")
        
        print(f"\n📋 Provider padrão para Vision: {ProjectConfig.DEFAULT_VISION_PROVIDER.value}")
        print("=" * 60)
