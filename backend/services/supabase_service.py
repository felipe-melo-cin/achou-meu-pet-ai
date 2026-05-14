import os
import uuid
import base64
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL", ""),
    os.environ.get("SUPABASE_ANON_KEY", ""),
)


def upload_image(file_bytes: bytes, extension: str) -> str:
    """Faz upload de imagem no bucket 'pet_images' e retorna a URL pública."""
    file_name = f"pets/{uuid.uuid4()}.{extension}"

    supabase.storage.from_("pet_images").upload(
        file_name,
        file_bytes,
        {"content-type": f"image/{extension}"},
    )

    res = supabase.storage.from_("pet_images").get_public_url(file_name)
    return res


def register_pet(pet_data: dict) -> dict:
    """Insere um pet no banco e retorna o registro criado."""
    response = supabase.table("pets").insert(pet_data).execute()
    return response.data[0] if response.data else {}


def search_similar_pets(embedding: list[float], threshold: float = 0.5, limit: int = 10) -> list[dict]:
    """Busca pets similares usando busca vetorial via RPC match_pets."""
    response = supabase.rpc("match_pets", {
        "query_embedding": embedding,
        "match_threshold": threshold,
        "match_count": limit,
    }).execute()
    return response.data or []


def register_user(email: str, password: str, metadata: dict) -> dict:
    """Cria usuário via Supabase Auth."""
    response = supabase.auth.sign_up({
        "email": email,
        "password": password,
        "options": {"data": metadata},
    })
    return {"user": str(response.user.id) if response.user else None}


def login_user(email: str, password: str) -> dict:
    """Autentica usuário e retorna access_token."""
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })
    return {
        "access_token": response.session.access_token if response.session else None,
        "user": str(response.user.id) if response.user else None,
    }
