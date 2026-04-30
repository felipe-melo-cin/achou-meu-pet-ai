import flet as ft

def tela_cadastro(page: ft.Page):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO

    # 🔥 função correta (AGORA TEM ACESSO AO PAGE)
    def ir_para_matches(e):
        from telas.matches import tela_matches
        tela_matches(page)

    # INPUTS
    cidade = ft.TextField(label="Cidade", bgcolor="#E8F3EC", border_radius=10, expand=True)
    animal = ft.TextField(label="Animal", bgcolor="#E8F3EC", border_radius=10, expand=True)
    sexo = ft.TextField(label="Sexo", bgcolor="#E8F3EC", border_radius=10, expand=True)

    data = ft.TextField(label="Data", bgcolor="#E8F3EC", border_radius=10, expand=True)
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
                descricao,
                ft.FilledButton(
                    "Cadastrar",
                    bgcolor="#2F5D62",
                    color="white",
                    width=float("inf"),
                    on_click=ir_para_matches  # ✅ agora funciona
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
                            on_click=ir_para_matches  # ✅ aqui também
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