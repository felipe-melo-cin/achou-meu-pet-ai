import flet as ft
import os
import json
from backend.ai.vision import VisionModel
from backend.ai.embeddings import EmbeddingModel
from backend.database.queries import registrar_pet_no_banco, gerar_link_temporario, atualizar_dados_pet

def tela_cadastro(page: ft.Page):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO
    
    estado_tela = {"caminho_imagem": None, "dados_visao": None}

    def ir_para_agradecimentos(e):
        # 1. Importa a função da tela de agradecimento
        from frontend.screens.agradecimento import tela_agradecimento
        # 2. Importa a função da tela inicial (ajuste o caminho se o nome da pasta/arquivo for outro)
        # Exemplo: se o arquivo tela_inicial.py estiver na mesma pasta 'screens':
        from frontend.screens.tela_inicial import tela_inicial 
        # 3. Chama a função passando a referência da tela inicial
        tela_agradecimento(page, tela_inicial)
        
    # INPUTS
    cidade = ft.TextField(label="Cidade", bgcolor="#E8F3EC", border_radius=10, expand=True)
    animal = ft.TextField(label="Animal", bgcolor="#E8F3EC", border_radius=10, expand=True)
    sexo = ft.TextField(label="Sexo", bgcolor="#E8F3EC", border_radius=10, expand=True)

    data = ft.TextField(label="Data", bgcolor="#E8F3EC", border_radius=10, expand=True)
    local = ft.TextField(label="Local exato", bgcolor="#E8F3EC", border_radius=10, expand=True)
    horario = ft.TextField(label="Horário", bgcolor="#E8F3EC", border_radius=10, expand=True)

    texto_imagem = ft.Text("Nenhuma imagem selecionada", color="red")

    # FILE PICKER LOGIC - adicionar ao overlay ANTES de usar
    def on_image_selected(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            caminho_local = e.files[0].path
            estado_tela["caminho_imagem"] = caminho_local
            texto_imagem.value = f"✓ Imagem selecionada: {e.files[0].name}"
            texto_imagem.color = "green"
            page.update()

            # 1. Enviar para o Vision Model para preencher o form
            try:
                vision = VisionModel()
                dados_json = vision.analyze_pet_image(caminho_local)
                estado_tela["dados_visao"] = dados_json
                
                # Preenchendo formulário com os dados da IA
                animal.value = dados_json.get("tipo_animal", "")
                descricao.value = f"Raça provável: {dados_json.get('raça_provável', '')}\nCores: {', '.join(dados_json.get('cores', []))}\nCaracterísticas: {dados_json.get('características', '')}"
                page.update()
            except Exception as ex:
                print(f"Erro na visão: {ex}")

    file_picker = ft.FilePicker()           # Criar vazio
    page.overlay.append(file_picker)        # Adicionar ao overlay

    # Definir callback DEPOIS
    file_picker.on_result = on_image_selected

    botao_anexar = ft.ElevatedButton(
        "Anexar Foto do Pet", 
        icon=ft.Icons.UPLOAD_FILE, 
        on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"])
    )
    
    # LOGICA DE CADASTRO FINAL
    def realizar_cadastro(e):
        if not estado_tela["caminho_imagem"]:
            texto_imagem.value = "❌ Por favor, anexe uma imagem antes de cadastrar!"
            texto_imagem.color = "red"
            page.update()
            return
        
        # Lê a imagem localmente
        with open(estado_tela["caminho_imagem"], "rb") as f:
            arquivo_bytes = f.read()
        
        nome_arquivo = os.path.basename(estado_tela["caminho_imagem"])
        status_pet = "perdido" # ou encontrado, dependendo da sua regra de negócio
        
        # 2. Registra no banco (Storage + Tabela)
        registrar_pet_no_banco(arquivo_bytes, nome_arquivo, status_pet)
        caminho_no_storage = f"{status_pet}/{nome_arquivo}"
        
        # 3. Pega o Link Temporário e Gera o Embedding
        link_temp = gerar_link_temporario(caminho_no_storage)
        embedding_model = EmbeddingModel()
        vetor = embedding_model.generate_image_vector(link_temp)
        
        # 4. Atualiza a tabela com o vetor gerado e a descrição
        if vetor:
            atualizar_dados_pet(caminho_no_storage, estado_tela["dados_visao"], vetor)
            
        ir_para_agradecimentos(e)
    
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
                    "Adicione o pet ao sistema com imagens e uma breve descrição clara, para que nossa IA realize matches com futuros tutores.",
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
                    on_click=realizar_cadastro
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
                            on_click=realizar_cadastro
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