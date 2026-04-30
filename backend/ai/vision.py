import json
import re
import base64
import mimetypes
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from pathlib import Path
import requests

from .config import (
    ModelConfig,
    APIProvider,
    APIConfigFactory,
    ProjectConfig
)

# ============================================================================
# CLASSE BASE ABSTRATA PARA VISION MODELS
# ============================================================================

class BaseVisionModel(ABC):
    """Classe base abstrata para modelos de visão"""
    
    def __init__(self, model: str, provider: APIProvider):
        self.model = model
        self.provider = provider
        self.config = APIConfigFactory.get_config(provider)
        self.client = self.config.get_client()
    
    @abstractmethod
    def analyze_pet_image(self, image_input: str) -> Dict[str, Any]:
        """Analisa imagem de animal e retorna características"""
        pass
    
    def _build_analysis_prompt(self) -> str:
        """Constrói o prompt para análise de animal"""
        return """
        Analise esta imagem de um animal de estimação e forneça as informações em formato JSON válido:
        {
            "tipo_animal": "cachorro/gato/outro",
            "cores": ["lista", "de", "cores"],
            "características": "descrição física distintiva",
            "raça_provável": "raça estimada ou 'desconhecida'",
            "tamanho_estimado": "pequeno/médio/grande",
            "idade_estimada": "filhote/adulto/idoso"
        }
        
        Importante:
        - Retorne APENAS o JSON válido, sem markdown ou explicações adicionais
        - Seja preciso e descritivo
        """

    def _is_url(self, path: str) -> bool:
        return path.startswith(('http://', 'https://'))

    def _get_mime_type(self, path: str) -> str:
        mime_type, _ = mimetypes.guess_type(path)
        return mime_type or 'image/jpeg'

    def _load_image_as_base64(self, path: str) -> str:
        image_data = Path(path).read_bytes()
        return base64.b64encode(image_data).decode('utf-8')

    @staticmethod
    def _parse_json_response(content: str) -> Dict[str, Any]:
        """Extrai e parseia o JSON da resposta, mesmo com texto extra."""
        try:
            # Procura por algo que pareça um bloco JSON usando regex
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(content)
        except Exception as e:
            raise ValueError(f"Falha ao extrair JSON: {e}\nConteúdo: {content}")


# ============================================================================
# IMPLEMENTAÇÃO DO OPENROUTER VISION
# ============================================================================

class OpenRouterVisionModel(BaseVisionModel):
    def __init__(self, model: str = ModelConfig.OPENROUTER_VISION.value):
        super().__init__(model, APIProvider.OPENROUTER)
    
    def analyze_pet_image(self, image_input: str) -> Dict[str, Any]:
        prompt = self._build_analysis_prompt()
        
        try:
            if self._is_url(image_input):
                # Alguns provedores no OpenRouter aceitam URL direta, 
                # mas passar em base64 é mais universal e seguro para APIs que falham em baixar URLs privadas.
                resp = requests.get(image_input)
                resp.raise_for_status()
                image_base64 = base64.b64encode(resp.content).decode("utf-8")
                mime_type = resp.headers.get('Content-Type', 'image/jpeg')
            else:
                image_base64 = self._load_image_as_base64(image_input)
                mime_type = self._get_mime_type(image_input)

            # Cliente OpenRouter (OpenAI SDK compatível)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}"
                            }
                        }
                    ],
                }]
            )
            return self._parse_json_response(response.choices[0].message.content)
        except Exception as e:
            raise RuntimeError(f"Erro OpenRouter: {str(e)}")


# ============================================================================
# CLASSE PRINCIPAL / FACTORY
# ============================================================================

class VisionModel(BaseVisionModel):
    """
    Classe principal que delega a lógica para o provider configurado
    """
    def __init__(self, model: Optional[str] = None, provider: Optional[APIProvider] = None):
        if provider is None:
            provider = ProjectConfig.DEFAULT_VISION_PROVIDER
        
        if model is None:
            if provider == APIProvider.GEMINI:
                model = ModelConfig.GEMINI_VISION.value
            else:
                model = ModelConfig.OPENROUTER_VISION.value
        
        super().__init__(model, provider)
    
    def analyze_pet_image(self, image_input: str) -> Dict[str, Any]:
        vision = OpenRouterVisionModel(self.model)
        
        return vision.analyze_pet_image(image_input)
