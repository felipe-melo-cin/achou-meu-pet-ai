import flet as ft
import os
import uuid # Para gerar nomes únicos na busca
from backend.ai.embeddings import EmbeddingModel
from backend.database.queries import comparar_pet
from backend.database.client import supabase # Para upload temporário

def tela_busca(page: ft.Page):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO

    estado_tela = {"caminho_imagem": None}
    
    def ir_para_matches(e):
        from frontend.screens.matches import tela_matches
        tela_matches(page)

    # INPUTS
    cidade = ft.TextField(label="Cidade", bgcolor="#E8F3EC", border_radius=10, expand=True)
    animal = ft.TextField(label="Animal", bgcolor="#E8F3EC", border_radius=10, expand=True)
    sexo = ft.TextField(label="Sexo", bgcolor="#E8F3EC", border_radius=10, expand=True)

    data = ft.TextField(label="Data do desaparecimento", bgcolor="#E8F3EC", border_radius=10, expand=True)
    local = ft.TextField(label="Local exato", bgcolor="#E8F3EC", border_radius=10, expand=True)
    horario = ft.TextField(label="Horário", bgcolor="#E8F3EC", border_radius=10, expand=True)
    
    texto_imagem = ft.Text("Nenhuma imagem selecionada", color="red")

    # FILE PICKER - adicionar ao overlay ANTES de usar
    def on_image_selected(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            estado_tela["caminho_imagem"] = e.files[0].path
            texto_imagem.value = f"✓ Imagem selecionada: {e.files[0].name}"
            texto_imagem.color = "green"
            page.update()

    file_picker = ft.FilePicker()           # Criar vazio
    page.overlay.append(file_picker)        # Adicionar ao overlay

    # Definir callback DEPOIS
    file_picker.on_result = on_image_selected

    botao_anexar = ft.ElevatedButton(
        "Anexar Foto para Busca", 
        icon=ft.Icons.UPLOAD_FILE, 
        on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"])
    )

    def realizar_busca(e):
        if not estado_tela["caminho_imagem"]:
            texto_imagem.value = "❌ Por favor, anexe uma imagem para buscar!"
            texto_imagem.color = "red"
            page.update()
            return
            
        # 1. Upload temporário para gerar a URL que o modelo de Embedding exige
        with open(estado_tela["caminho_imagem"], "rb") as f:
            arquivo_bytes = f.read()
            
        nome_temp = f"temp_{uuid.uuid4().hex}.jpg"
        caminho_storage_temp = f"temporario/{nome_temp}"
        
        # Subindo direto pelo cliente supabase (já que não vai pra tabela)
        supabase.storage.from_("pets").upload(
            path=caminho_storage_temp, 
            file=arquivo_bytes,
            file_options={"content-type": "image/jpeg"}
        )
        
        # 2. Pegar URL temporária
        res = supabase.storage.from_("pets").create_signed_url(caminho_storage_temp, 60) # 1 min é o suficiente
        link_temp = res["signedURL"] if isinstance(res, dict) else res
        
        # 3. Gerar o Embedding
        embedding_model = EmbeddingModel()
        vetor_busca = embedding_model.generate_image_vector(link_temp)
        
        # 4. Apagar a imagem temporária do Storage para não ocupar espaço
        supabase.storage.from_("pets").remove([caminho_storage_temp])
        
        # 5. Procurar os similares no Banco
        if vetor_busca:
            # OBS: Ajuste no seu Supabase a RPC 'buscar_pets_similares' para aceitar threshold (ex: 0.70) 
            # ou modifique a query em queries.py
            resultados_similares = comparar_pet(vetor_busca)
            
            print(f"Encontrados {len(resultados_similares)} pets parecidos!")
            
            # Aqui você pode enviar os "resultados_similares" para sua tela de matches
            # from screens.matches import tela_matches
            # tela_matches(page, resultados=resultados_similares)
            ir_para_matches(e)

    descricao = ft.TextField(
        label="Descrição",
        multiline=True,
        min_lines=5,
        max_lines=8,
        hint_text="Faça uma descrição objetiva do animal...",
        border_radius=15
    )

    def voltar(e):
        from frontend.screens.tela_inicial import tela_inicial
        tela_inicial(page)

    # LADO ESQUERDO
    left_side = ft.Container(
        bgcolor="#DCEDE5",
        padding=20,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar),
                ft.Text(
                    "Envie uma foto do pet, juntamente com uma descrição objetiva do animal e nossa IA irá comparar com imagens já cadastradas para encontrar possíveis correspondências.",
                    size=16,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Image(
                    src="pata.png",
                    width=50,
                    height=50,
                    fit="contain"
                )
            ]
        )
    )

    # FORMULÁRIO
    if page.width < 600:
        form = ft.Column(
            spacing=15,
            controls=[
                cidade,
                animal,
                sexo,
                data,
                local,
                horario,
                botao_anexar,
                texto_imagem,
                descricao,
                ft.FilledButton(
                    "Cadastrar",
                    bgcolor="#2F5D62",
                    color="white",
                    width=float("inf"),
                    on_click=realizar_busca
                )
            ]
        )
    else:
        form = ft.Column(
            controls=[
                ft.Row([cidade, animal, sexo], spacing=10),
                ft.Row([data, local, horario], spacing=10),
                botao_anexar,
                texto_imagem,
                descricao,
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.FilledButton(
                            "Cadastrar",
                            bgcolor="#2F5D62",
                            color="white",
                            on_click=realizar_busca
                        )
                    ]
                )
            ]
        )

    right_side = ft.Container(
        padding=20,
        expand=True,
        content=form
    )

    # RESPONSIVIDADE
    if page.width < 600:
        layout = ft.Column([left_side, right_side])
    else:
        layout = ft.Row(
            expand=True,
            controls=[
                ft.Container(width=250, content=left_side),
                right_side
            ]
        )

    page.add(layout)
    page.update()