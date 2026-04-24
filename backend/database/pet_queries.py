import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Inicialização limpa do cliente
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"), 
    os.getenv("SUPABASE_KEY")
)

def registrar_pet_no_banco(arquivo_bytes: bytes, nome_arquivo: str, status: str):
    # o upload da imagem e criação do registro no banco
    try:
        caminho_no_storage = f"{status}/{nome_arquivo}"
        
        # upload para o storage
        supabase.storage.from_("pets").upload(
            path=caminho_no_storage, 
            file=arquivo_bytes,
            file_options={"content-type": "image/jpeg"} # Idealmente detectar o tipo real
        )
        
        # Registro na Tabela
        dados = {
            "status": status,
            "foto_caminho": caminho_no_storage,
            "descricao_json": None, # Placeholder 
            "pet_vector": None      # Placeholder 
        }
        
        return supabase.table("pets").insert(dados).execute()
        
    except Exception as e:
        raise RuntimeError(f"Falha na integração com Supabase: {str(e)}")
    


def comparar_pet(vetor_da_nova_foto):
    rpc_res = supabase.rpc("buscar_pets_similares", {
        "query_embedding": vetor_da_nova_foto,
        "match_threshold": 0.5, # 50% de similaridade mínima
        "match_count": 5        # Top 5 resultados
    }).execute()
    
    return rpc_res.data