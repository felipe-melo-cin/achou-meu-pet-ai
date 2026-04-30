import flet as ft

def tela_agradecimento(page: ft.Page, ir_para_inicio):
    page.clean()
    page.bgcolor = "#FFFFFF"

    header = ft.Row([
        ft.TextButton(
            "Achou meu pet AI?",
            on_click=lambda e: ir_para_inicio(page),
            style=ft.ButtonStyle(color="#2F5D62")
        )
    ])

    conteudo_central = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),  # centro exato
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Obrigado por contribuir!",
                    size=32,
                    weight="bold",
                    color="#2F5D62",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Sua ação pode reunir um pet ao seu tutor.",
                    size=18,
                    color="#2F5D62",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Voltar ao Início",
                    on_click=lambda e: ir_para_inicio(page),
                    bgcolor="#7DD2A8",
                    color="white"
                )
            ]
        )
    )

    
    layout = ft.Column(
        expand=True,
        controls=[
            header,
            conteudo_central
        ]
    )

    page.add(layout)
    page.update()