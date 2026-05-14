import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

def pet_vision_analysis(base64_image: str) -> dict:
    """Analisa uma imagem de pet e retorna JSON com espécie, raça, cor e marcas."""
    response = client.chat.completions.create(
        model="baidu/qianfan-ocr-fast:free",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Analyze this image of a pet and return a JSON object with: "
                        "species, breed (or 'unknown'), primaryColor, distinguishingMarks. "
                        "Return ONLY valid JSON, nothing else."
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("IA não retornou conteúdo.")

    clean = re.sub(r"```(?:json)?", "", content).strip().rstrip("`").strip()
    return json.loads(clean)


def generate_embedding(base64_image: str) -> list[float]:
    """Gera um embedding vetorial a partir da análise visual do pet."""
    vision = pet_vision_analysis(base64_image)
    text = f"{vision.get('species','')} {vision.get('breed','')} {vision.get('primaryColor','')} {vision.get('distinguishingMarks','')}".strip()

    response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding
