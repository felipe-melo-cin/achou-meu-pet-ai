import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Inicialização limpa do cliente
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"), 
    os.getenv("SUPABASE_KEY")
)

def gerar_link_temporario(caminho_no_storage: str):
    # Cria um link que funciona por apenas 15 minutos (900 segundos)
    # Essencial para o Dev 1 enviar para a API de Vision
    res = supabase.storage.from_("pets").create_signed_url(caminho_no_storage, 900)
    if isinstance(res, dict) and "signedURL" in res:
        return res["signedURL"]
    
    return res
