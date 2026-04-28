print("Importing BaseModel...")

from abc import ABC, abstractmethod
from openai import OpenAI
import os
import dotenv

class BaseModel(ABC):

    def __init__(self, model: str) -> None:

        # Carrega as variáveis de ambiente
        dotenv.load_dotenv()

        # Coleta a chave da API nas variáveis de ambiente
        self.API_KEY = os.getenv("MODEL_API_KEY")
        self.model = model

        # Gera o cliente com base na chave da API
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.API_KEY,
        )

    @abstractmethod
    def make_request(self, request: str | list[str], single_request: bool = True)\
            -> list[float] | list[list[float] | None] | None:
        pass
