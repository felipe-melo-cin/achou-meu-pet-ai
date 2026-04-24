from fastapi import FastAPI, UploadFile, File, HTTPException
from database.pet_queries import registrar_pet_no_banco
from database.url_queries import gerar_link_temporario


app = FastAPI(title="Achou Meu Pet AI API", description="Infraestrutura base para busca de pets")


@app.post("/upload-pet/{status}")
async def upload_pet(status: str, file: UploadFile = File(...)):
    # Validação simples de status
    if status not in ["perdido", "achado"]:
        raise HTTPException(status_code=501, detail="Status deve ser 'perdido' ou 'achado'")

    try:
        conteudo = await file.read()
        resultado = registrar_pet_no_banco(conteudo, file.filename, status)
        
        return {
            "mensagem": "Registro criado com sucesso",
            "dados": resultado.data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/processar-pet/{status}")
async def processar_pet(status: str, file: UploadFile = File(...)):

    conteudo = await file.read()
    res_storage = registrar_pet_no_banco(conteudo, file.filename, status)
    print(res_storage)
    caminho = res_storage.data[0]['foto_caminho']
    
    # Gera o link para os outros Devs usarem
    url_temporaria = gerar_link_temporario(caminho)

    # --- PASSO 2: TRABALHO DO DEV (IA/Vision) ---
    # Aqui o Dev 1 vai chamar a função dele: 
    # resultado_ia = dev1.analisar_imagem(url_temporaria)
    
    # --- PASSO 3: TRABALHO DO DEVS (Embeddings) ---
    # Aqui o Dev 2 vai chamar a função dele:
    # vetor = dev2.gerar_vetor(url_temporaria)

    # --- PASSO 4: SEU TRABALHO (DB Update) ---
    # Atualizar a linha no banco com a descrição e o vetor que eles geraram
    
    return {"status": "Aguardando integração dos Devs 1 e 2", "url_para_ia": url_temporaria}
