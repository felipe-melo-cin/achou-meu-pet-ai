print("Importing ImageToVectorModel...")

from .BaseModel import BaseModel

class ImageUrlToVectorModel(BaseModel):

    def __init__(self, model: str) -> None:
        super().__init__(model)

    def generate_image_vector(self, image_url: str) -> list[float]:
        """Gera um vetor com base no url de imagem fornecido"""
        embedding = self.client.embeddings.create(
            model=self.model,
            input=[{
                "content": [{
                    "type": "image_url",
                    "image_url": {"url": image_url}
                }]
            }],
            encoding_format="float"
        )
        return embedding.data[0].embedding
