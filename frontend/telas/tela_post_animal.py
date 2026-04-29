# tela_post_animal.py
import flet as ft

def tela_post_animal(page: ft.Page):

    page.clean()

    page.bgcolor = "#f5f5f5"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # IMPORTANTE
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    # VOLTAR PARA MATCHES
    def voltar(e):
        from tela_matches import tela_matches
        tela_matches(page)

    post = ft.Container(
        width=600,
        bgcolor="white",
        border_radius=20,
        padding=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            spacing=15,
            controls=[

                # TOPO
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.CircleAvatar(
                            foreground_image_src="https://i.pravatar.cc/100?img=5",
                            radius=20
                        ),

                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text(
                                    "@Camila_Mendes",
                                    weight=ft.FontWeight.BOLD,
                                    size=14
                                ),
                            ]
                        )
                    ]
                ),

                # INFORMAÇÕES
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Data que foi encontrado:",
                                    weight=ft.FontWeight.BOLD,
                                    size=12
                                ),
                                ft.Text("24/03/26 (hoje)", size=12)
                            ]
                        ),

                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Local exato:",
                                    weight=ft.FontWeight.BOLD,
                                    size=12
                                ),
                                ft.Text(
                                    "Parque da Jaqueira, Recife PE "
                                    "(em frente à igreja branca)",
                                    size=12
                                )
                            ]
                        ),

                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Horário:",
                                    weight=ft.FontWeight.BOLD,
                                    size=12
                                ),
                                ft.Text("16h:12", size=12)
                            ]
                        ),
                    ]
                ),

                # DESCRIÇÃO
                ft.Text(
                    "Golden encontrado no Parque da Jaqueira. "
                    "Muito dócil e bem treinado, responde ao "
                    "comando como: “Senta”, “Me dá a patinha”.",
                    size=18,
                    weight=ft.FontWeight.W_500,
                ),

                # IMAGENS
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            border_radius=15,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            content=ft.Image(
                                src="https://placedog.net/300/250?id=1",
                                width=220,
                                height=180,
                            )
                        ),

                        ft.Container(
                            border_radius=15,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            content=ft.Image(
                                src="https://placedog.net/300/250?id=2",
                                width=220,
                                height=180,
                            )
                        ),
                    ]
                ),

                # BOTÃO
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.ElevatedButton(
                            "Contatar anunciante",
                            bgcolor="#74d3b0",
                            color="white",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=20,
                            )
                        )
                    ]
                )
            ]
        )
    )

    page.add(

        # BOTÃO VOLTAR
        ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=voltar
        ),

        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[post]
        )
    )

    page.update()