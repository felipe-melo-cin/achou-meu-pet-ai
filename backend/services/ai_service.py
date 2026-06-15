import os
import json
import re
import requests
from dotenv import load_dotenv
from errors import ExternalServiceError

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")


def pet_vision_analysis(base64_image: str) -> dict:
    """
    Envia a imagem codificada em base64 para o modelo de visão livre do OpenRouter.
    Retorna uma descrição estruturada em formato JSON.
    """
    if not OPENROUTER_API_KEY:
        raise ExternalServiceError("Chave da API do OpenRouter não encontrada.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://achoumeupetai.com",
        "X-Title": "Achou Meu Pet"
    }

    # Restaurado o modelo solicitado. Removido 'response_format' para evitar erros 400/404 
    # de parâmetros não suportados por este modelo de OCR específico no OpenRouter.
    payload = {
        "model": "nex-agi/nex-n2-pro:free",
        "messages": [{
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
        }]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Se a API retornar erro, extraímos a mensagem detalhada de resposta do OpenRouter
        if response.status_code != 200:
            try:
                err_data = response.json()
                err_msg = err_data.get("error", {}).get("message", response.text)
            except Exception:
                err_msg = response.text
            raise ExternalServiceError(f"Erro na API do OpenRouter (Status {response.status_code}): {err_msg}")

        res_data = response.json()
        content = res_data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as re_err:
        raise ExternalServiceError(f"Erro na requisição para análise visual de IA: {str(re_err)}")
    except (KeyError, IndexError) as parse_err:
        raise ExternalServiceError(f"Resposta de análise de visão veio em um formato inesperado: {str(parse_err)}")

    if not content:
        raise ExternalServiceError("O modelo de visão de IA não retornou nenhum conteúdo válido.")

    # Remove eventuais marcações de bloco de código markdown de forma limpa
    clean = content.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^json)?\s*", "", clean)
        clean = re.sub(r"\s*```$", "", clean)
    clean = clean.strip()

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        # Fallback inteligente procurando as chaves { ... } usando a variável 'content' correta
        match_braces = re.search(r"(\{.*\})", content, re.DOTALL)
        if match_braces:
            try:
                return json.loads(match_braces.group(1).strip())
            except json.JSONDecodeError as json_err:
                raise ExternalServiceError(
                    f"Resposta de IA malformada para decodificação em JSON: {str(json_err)}. "
                    f"Conteúdo bruto retornado: {content}"
                )
        
        raise ExternalServiceError(f"Nenhum bloco de dados JSON válido foi encontrado no retorno da IA. Conteúdo bruto: {content}")


def generate_embedding(base64_image: str) -> list[float]:
    """
    Gera um embedding vetorial direto da imagem usando o modelo nvidia/llama-nemotron-embed-vl-1b-v2:free.
    Bypassa o fluxo textual e gera um vetor direto a partir da visão computacional de forma gratuita.
    """
    if not OPENROUTER_API_KEY:
        raise ExternalServiceError("Chave da API do OpenRouter não encontrada.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "[https://achoumeupetai.com](https://achoumeupetai.com)",
        "X-Title": "Achou Meu Pet"
    }

    api_url = "https://openrouter.ai/api/v1/embeddings"

    # Passamos o input de forma multimodal utilizando uma instrução genérica juntamente com a imagem do pet.
    payload = {
        "model": "nvidia/llama-nemotron-embed-vl-1b-v2:free",
        "input": [
            {
                "content": [
                    {
                        "type": "text",
                        "text": "A photo of a lost or found pet."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Tratamento de erro robusto para a rota de embeddings
        if response.status_code != 200:
            try:
                err_data = response.json()
                err_msg = err_data.get("error", {}).get("message", response.text)
            except Exception:
                err_msg = response.text
            raise ExternalServiceError(f"Erro na API do OpenRouter ao gerar embeddings (Status {response.status_code}): {err_msg}")

        res_data = response.json()
        
        # Garante a extração correta do vetor gerado
        embedding = res_data["data"][0]["embedding"]
        return embedding
    except requests.exceptions.RequestException as re_err:
        raise ExternalServiceError(f"Falha de comunicação para a geração de embeddings visuais: {str(re_err)}")
    except (KeyError, IndexError) as parse_err:
        raise ExternalServiceError(f"O payload de embeddings retornou uma estrutura inesperada: {str(parse_err)}")