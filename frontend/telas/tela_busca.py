import flet as ft

def tela_busca(page: ft.Page):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO

    def ir_para_agradecimentos(e):
        # 1. Importa a função da tela de agradecimento
        from telas.agradecimento import tela_agradecimento
        # 2. Importa a função da tela inicial (ajuste o caminho se o nome da pasta/arquivo for outro)
        # Exemplo: se o arquivo tela_inicial.py estiver na mesma pasta 'telas':
        from telas.tela_inicial import tela_inicial 
        # 3. Chama a função passando a referência da tela inicial
        tela_agradecimento(page, tela_inicial)

        
    # INPUTS
    cidade = ft.TextField(label="Cidade", bgcolor="#E8F3EC", border_radius=10, expand=True)
    animal = ft.TextField(label="Animal", bgcolor="#E8F3EC", border_radius=10, expand=True)
    sexo = ft.TextField(label="Sexo", bgcolor="#E8F3EC", border_radius=10, expand=True)

    data = ft.TextField(label="Data do desaparecimento", bgcolor="#E8F3EC", border_radius=10, expand=True)
    local = ft.TextField(label="Local exato", bgcolor="#E8F3EC", border_radius=10, expand=True)
    horario = ft.TextField(label="Horário", bgcolor="#E8F3EC", border_radius=10, expand=True)

    descricao = ft.TextField(
        label="Descrição",
        multiline=True,
        min_lines=5,
        max_lines=8,
        hint_text="Faça uma descrição objetiva do animal...",
        border_radius=15
    )

    def voltar(e):
        from telas.tela_inicial import tela_inicial
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
                descricao,
                ft.FilledButton(
                    "Cadastrar",
                    bgcolor="#2F5D62",
                    color="white",
                    width=float("inf"),
                    on_click=ir_para_agradecimentos  # ✅ agora funciona
                )
            ]
        )
    else:
        form = ft.Column(
            controls=[
                ft.Row([cidade, animal, sexo], spacing=10),
                ft.Row([data, local, horario], spacing=10),
                descricao,
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.FilledButton(
                            "Cadastrar",
                            bgcolor="#2F5D62",
                            color="white",
                            on_click=ir_para_agradecimentos  # ✅ aqui também
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