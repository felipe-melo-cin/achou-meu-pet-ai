# /backend/ai/pipeline.py
from typing import Dict, Any, List
from .embeddings import EmbeddingModel
from .vision import VisionModel

class PetProcessingPipeline:
    """
    Orquestra o processamento completo de uma imagem de pet:
    1. Análise visual (características)
    2. Geração de embedding
    3. Preparação para banco de dados
    """
    
    def __init__(self):
        self.vision_model = VisionModel()
        self.embedding_model = EmbeddingModel()
    
    def process_pet_image(self, image_url: str) -> Dict[str, Any]:
        """
        Pipeline completo de processamento
        
        Args:
            image_url: URL da imagem (pode ser URL assinada Supabase)
        
        Returns:
            {
                "descricao": {...},  # Análise visual
                "embedding": [...],  # Vetor para busca
                "status": "sucesso"
            }
        """
        try:
            # 1. Análise visual detalhada
            print(f"[1/2] Analisando imagem...")
            descricao = self.vision_model.analyze_pet_image(image_url)
            
            # 2. Gera embedding
            print(f"[2/2] Gerando embedding...")
            embedding = self.embedding_model.generate_image_vector(image_url)
            
            return {
                "descricao": descricao,
                "embedding": embedding,
                "status": "sucesso"
            }
        
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": str(e)
            }
    
    def process_batch(self, image_urls: List[str]) -> List[Dict]:
        """Processa múltiplas imagens"""
        return [self.process_pet_image(url) for url in image_urls]