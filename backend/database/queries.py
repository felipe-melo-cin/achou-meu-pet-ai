import os
from dotenv import load_dotenv
from . import client
from .client import supabase 

load_dotenv()


def registrar_pet_no_banco(arquivo_bytes: bytes, nome_arquivo: str, status: str):
    # o upload da imagem e criação do registro no banco
    try:
        caminho_no_storage = f"{status}/{nome_arquivo}"
        
        # upload para o storage
        supabase.storage.from_("pets").upload(
            path=caminho_no_storage, 
            file=arquivo_bytes,
            file_options={"content-type": "image/jpeg", "upsert": "true"} # Idealmente detectar o tipo real
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



def gerar_link_temporario(caminho_no_storage: str):
    # Cria um link que funciona por apenas 15 minutos (900 segundos)
    # Essencial para o Dev 1 enviar para a API de Vision
    res = supabase.storage.from_("pets").create_signed_url(caminho_no_storage, 900)
    if isinstance(res, dict) and "signedURL" in res:
        return res["signedURL"]
    
    return res

def atualizar_dados_pet(caminho_no_storage: str, descricao_json: dict, pet_vector: list):
    """Atualiza o registro do pet com o vetor gerado e os dados da IA de visão"""
    try:
        return supabase.table("pets").update({
            "descricao_json": descricao_json,
            "pet_vector": pet_vector
        }).eq("foto_caminho", caminho_no_storage).execute()
    except Exception as e:
        raise RuntimeError(f"Falha ao atualizar dados do pet: {str(e)}")