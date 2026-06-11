import os
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL", ""),
    os.environ.get("SUPABASE_ANON_KEY", ""),
)

# Colunas reais da tabela pets:
# id, species, breed, color, description, lastLocation, contactInfo, imageUrl, embedding, created_at


def upload_image(file_bytes: bytes, extension: str) -> str:
    """Faz upload no bucket 'pet_images' e retorna URL pública."""
    file_name = f"pets/{uuid.uuid4()}.{extension}"
    supabase.storage.from_("pet_images").upload(
        file_name,
        file_bytes,
        {"content-type": f"image/{extension}"},
    )
    return supabase.storage.from_("pet_images").get_public_url(file_name)


def register_pet(pet_data: dict) -> dict:
    """Insere um pet e retorna o registro criado."""
    # Garante que só manda colunas que existem na tabela
    allowed = {'species', 'breed', 'color', 'description', 'lastLocation', 'contactInfo', 'imageUrl', 'embedding'}
    clean   = {k: v for k, v in pet_data.items() if k in allowed}
    response = supabase.table("pets").insert(clean).execute()
    return response.data[0] if response.data else {}


def list_pets(limit: int = 50) -> list:
    """Retorna os pets mais recentes para o feed."""
    response = (
        supabase.table("pets")
        .select("id, species, breed, color, description, lastLocation, contactInfo, imageUrl, created_at")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    rows = response.data or []
    for r in rows:
        # Normaliza created_at → createdAt para o frontend
        r['createdAt'] = r.pop('created_at', None)
        # Mapeia color → primaryColor para compatibilidade com o frontend
        r['primaryColor'] = r.get('color', '')
    return rows


def search_similar_pets(embedding: list, threshold: float = 0.5, limit: int = 10) -> list:
    """Busca pets similares via RPC match_pets (pgvector)."""
    response = supabase.rpc("match_pets", {
        "query_embedding": embedding,
        "match_threshold": threshold,
        "match_count":     limit,
    }).execute()
    rows = response.data or []
    for r in rows:
        r['createdAt']    = r.pop('created_at', None)
        r['primaryColor'] = r.get('color', '')
    return rows


def register_user(email: str, password: str, metadata: dict) -> dict:
    response = supabase.auth.sign_up({
        "email":    email,
        "password": password,
        "options":  {"data": metadata},
    })
    if not response.user:
        raise ValueError("Falha ao criar usuário.")
    
    # Avisa se precisa confirmar email
    email_confirmed = response.user.email_confirmed_at is not None
    return {
        "user_id": str(response.user.id),
        "email_confirmation_required": not email_confirmed,
    }


def login_user(email: str, password: str) -> dict:
    """Autentica e retorna access_token."""
    response = supabase.auth.sign_in_with_password({
        "email":    email,
        "password": password,
    })
    if not response.session:
        raise ValueError("Email ou senha incorretos.")
    return {
        "access_token": response.session.access_token,
        "user_id":      str(response.user.id),
        "nome":         response.user.user_metadata.get("nome", ""),
    }
