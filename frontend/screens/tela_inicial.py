import flet as ft

def tela_inicial(page: ft.Page):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO

    #  navegação
    def abrir_cadastro(e):
        from screens.tela_cadastro import tela_cadastro
        tela_cadastro(page)
    
    def abrir_procurar(a):
        from screens.tela_busca import tela_busca
        tela_busca(page)

    #  BOTÃO LOGIN
    btn_login = ft.FilledButton(
        "Login",
        bgcolor="#7DD2A8",
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
        )
    )

    #  HEADER (AGORA SIMPLES)
    header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Image(src="lupa.png", width=50),
            btn_login
        ]
    )

    # MAIN
    main_section = ft.ResponsiveRow(
        controls=[
            ft.Column(col={"sm": 12, "md": 6}, controls=[
                ft.Text("Achou meu pet AI?", size=65, weight=ft.FontWeight.BOLD, color="#2F5D62"),
                ft.Text(size=22, spans=[
                    ft.TextSpan("Você encontrou ou está procurando um pet? \nNós ajudamos a "),
                    ft.TextSpan("reconectar vocês.", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ]),
                ft.Container(height=30),
                ft.Row([
                    ft.FilledButton("Procurar meu Pet", bgcolor="#7DD2A8", height=45, on_click=abrir_procurar),
                    ft.FilledButton(
                        "Cadastrar um Pet",
                        bgcolor="#7DD2A8",
                        height=45,
                        on_click=abrir_cadastro
                    ),
                ], spacing=20),
            ]),
            ft.Column(col={"sm": 12, "md": 6}, controls=[
                ft.Image(src="pets_ilustracao.png", width=300)
            ])
        ]
    )

    # FOOTER
    footer = ft.ResponsiveRow(
        controls=[
            ft.Text("Como funciona?", size=30, weight=ft.FontWeight.BOLD, color="#2F5D62", col=12),
            ft.Column(col=4, controls=[
                ft.Text("1. Perdeu ou Encontrou?", weight=ft.FontWeight.BOLD),
                ft.Text("(Use a busca ou cadastre)")
            ]),
            ft.Column(col=4, controls=[
                ft.Text("2. Detalhes Importantes.", weight=ft.FontWeight.BOLD),
                ft.Text("(Adiciona fotos e local)")
            ]),
            ft.Column(col=4, controls=[
                ft.Text("3. Reencontro Feliz.", weight=ft.FontWeight.BOLD),
                ft.Text("(Nossa IA aumenta as chances)")
            ]),
        ]
    )

    # LAYOUT
    page.add(
        ft.Container(
            padding=20,
            content=ft.Column([
                header,
                ft.Container(height=50),
                main_section,
                ft.Container(height=80),
                footer
            ])
        )
    )

    page.update()