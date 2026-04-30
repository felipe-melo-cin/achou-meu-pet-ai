print("Importing EmbeddingModel...")

from .base import BaseModel

class EmbeddingModel(BaseModel):

    def __init__(self, model: str) -> None:
        super().__init__(model)

    def make_request(self, request: str | list[str], single_request: bool = True)\
            -> list[float] | list[list[float] | None] | None:
        """Faz uma requisição de geração de vetor ou lista de vetores com base em URLs de imagens"""

        try:

            if single_request:

                if not isinstance(request, str):
                    raise TypeError

                return self.generate_image_vector(request)

            else: # if not single_request

                if not isinstance(request, list):
                    raise TypeError

                return self.generate_image_vector_list(request)

        except TypeError:
            print("TypeError em make_request(): Tipo do pedido não foi o tipo esperado")

        except Exception as e:
            print(f"Ocorreu um erro inesperado em make_request(): {e}")

        return None

    def generate_image_vector(self, image_url: str) -> list[float] | None:
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

        try:
            return embedding.data[0].embedding

        except TypeError:

            try:
                error_message = embedding.error["message"]
                error_code = embedding.error["code"]
                print(f"Ocorreu um erro durante a formação do vetor em generate_image_vector(): {error_message}")
                print(f"Código de erro do embedding: {error_code}")

            except Exception as e:
                print(f"Ocorreu um erro inesperado em generate_image_vector(): {e}")

        except Exception as e:
            print(f"Ocorreu um erro inesperado em generate_image_vector(): {e}")

        return None

    def generate_image_vector_list(self, image_url_list: list[str]) -> list[list[float] | None]:
        """Gera vários vetores com base na lista de url de imagem fornecida"""
        vector_list = []

        for image_url in image_url_list:
            vector = self.generate_image_vector(image_url)
            vector_list.append(vector)

        return vector_list
