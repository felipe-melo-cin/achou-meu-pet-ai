# /backend/ai/vision.py
from typing import Dict, Any
from .base import BaseAIModel
from .config import ModelConfig

class VisionModel(BaseAIModel):
    """Analisa imagens e extrai características descritivas"""
    
    def __init__(self, model: str = ModelConfig.VISION_MODEL.value):
        """
        Args:
            model: Modelo de visão a usar (ex: gpt-4-vision)
        """
        super().__init__(model)
    
    def analyze_pet_image(self, image_url: str) -> Dict[str, Any]:
        """
        Analisa uma imagem de pet e extrai características
        
        Args:
            image_url: URL da imagem do pet
        
        Returns:
            Dict com:
            - tipo_animal: "cachorro", "gato", etc
            - cores: ["marrom", "branco"]
            - características: "manchas pretas nas orelhas"
            - raça_provável: "Labrador"
            - tamanho_estimado: "grande"
        
        Example:
            >>> vision = VisionModel()
            >>> resultado = vision.analyze_pet_image("https://...")
            >>> print(resultado['tipo_animal'])
            'cachorro'
        """
        
        prompt = """
        Analise esta imagem de um animal de estimação e forneça as informações em formato JSON:
        {
            "tipo_animal": "cachorro/gato/outro",
            "cores": ["lista", "de", "cores"],
            "características": "descrição física distintiva",
            "raça_provável": "raça estimada ou 'desconhecida'",
            "tamanho_estimado": "pequeno/médio/grande",
            "idade_estimada": "filhote/adulto/idoso"
        }
        Seja preciso e descritivo.
        """
        
        response = self.client.messages.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }],
            max_tokens=500
        )
        
        # Parse JSON da resposta
        import json
        try:
            # Tenta extrair JSON da resposta
            content = response.content[0].text
            # Remove markdown code blocks se existirem
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except (json.JSONDecodeError, AttributeError) as e:
            raise ValueError(f"Erro ao parsear resposta Vision: {str(e)}")