import os
import uuid
import logging
from supabase import create_client, Client
from dotenv import load_dotenv
from errors import DatabaseIntegrationError

load_dotenv()

# Instanciação global segura
try:
    supabase: Client = create_client(
        os.environ.get("SUPABASE_URL", ""),
        os.environ.get("SUPABASE_ANON_KEY", ""),
    )
except Exception as e:
    logging.critical(f"Falha de inicialização crítica do SDK Supabase: {str(e)}", exc_info=True)
    supabase = None


def upload_image(file_bytes: bytes, extension: str) -> str:
    """Faz upload no bucket 'pet_images' e retorna URL pública."""
    if not supabase:
        raise DatabaseIntegrationError("Cliente de banco de dados não inicializado ou indisponível.")

    file_name = f"pets/{uuid.uuid4()}.{extension}"
    try:
        supabase.storage.from_("pet_images").upload(
            file_name,
            file_bytes,
            {"content-type": f"image/{extension}"},
        )
        return supabase.storage.from_("pet_images").get_public_url(file_name)
    except Exception as e:
        raise DatabaseIntegrationError(f"Erro ao salvar arquivo de imagem no armazenamento: {str(e)}")


def register_pet(pet_data: dict) -> dict:
    """Insere um pet e retorna o registro criado."""
    if not supabase:
        raise DatabaseIntegrationError("Cliente de banco de dados não inicializado ou indisponível.")

    allowed = {'species', 'breed', 'color', 'description', 'lastLocation', 'contactInfo', 'imageUrl', 'embedding'}
    clean = {k: v for k, v in pet_data.items() if k in allowed}
    try:
        response = supabase.table("pets").insert(clean).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        raise DatabaseIntegrationError(f"Erro ao inserir pet no banco de dados relacional: {str(e)}")


def list_pets(limit: int = 50) -> list:
    """Retorna os pets mais recentes para o feed."""
    if not supabase:
        raise DatabaseIntegrationError("Cliente de banco de dados não inicializado ou indisponível.")

    try:
        response = (
            supabase.table("pets")
            .select("id, species, breed, color, description, lastLocation, contactInfo, imageUrl, created_at")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        rows = response.data or []
        for r in rows:
            # Normalização de chaves para compatibilidade com o frontend estático
            r['createdAt'] = r.pop('created_at', None)
            r['primaryColor'] = r.get('color', '')
        return rows
    except Exception as e:
        raise DatabaseIntegrationError(f"Erro ao recuperar feed de pets do banco de dados: {str(e)}")


def search_similar_pets(embedding: list, threshold: float = 0.5, limit: int = 10) -> list:
    """Busca pets similares via RPC match_pets (pgvector)."""
    if not supabase:
        raise DatabaseIntegrationError("Cliente de banco de dados não inicializado ou indisponível.")

    try:
        response = supabase.rpc("match_pets", {
            "query_embedding": embedding,
            "match_threshold": threshold,
            "match_count":     limit,
        }).execute()
        rows = response.data or []
        for r in rows:
            r['createdAt'] = r.pop('created_at', None)
            r['primaryColor'] = r.get('color', '')
        return rows
    except Exception as e:
        raise DatabaseIntegrationError(f"Falha de processamento na consulta por similaridade vetorial (pgvector): {str(e)}")


def register_user(email: str, password: str, metadata: dict) -> dict:
    if not supabase:
        raise DatabaseIntegrationError("Cliente de banco de dados não inicializado ou indisponível.")

    try:
        response = supabase.auth.sign_up({
            "email":    email,
            "password": password,
            "options":  {"data": metadata},
        })
        if not response.user:
            raise ValueError("Falha ao registrar novo usuário.")
        
        email_confirmed = response.user.email_confirmed_at is not None
        return {
            "user_id": str(response.user.id),
            "email_confirmation_required": not email_confirmed,
        }
    except Exception as e:
        raise DatabaseIntegrationError(f"Erro durante o cadastro de usuário no provedor de Auth: {str(e)}")


def login_user(email: str, password: str) -> dict:
    """Autentica e retorna access_token."""
    if not supabase:
        raise DatabaseIntegrationError("Cliente de banco de dados não inicializado ou indisponível.")

    try:
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
    except Exception as e:
        # Diferencia credenciais inválidas de erros reais de rede/banco
        if "invalid" in str(e).lower() or "credentials" in str(e).lower() or "claim" in str(e).lower():
            raise ValueError("Email ou senha incorretos.")
        raise DatabaseIntegrationError(f"Erro durante a autenticação de login no provedor de Auth: {str(e)}")