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

    # VOLTAR
    def voltar(e):
        from telas.matches import tela_matches
        tela_matches(page)

    # =========================
    # TOPO
    # =========================
    topo = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.CircleAvatar(
                foreground_image_src="https://i.pravatar.cc/100?img=5",
                radius=20
            ),

            ft.Text(
                "@Camila_Mendes",
                weight=ft.FontWeight.BOLD,
                size=14
            )
        ]
    )

    # =========================
    # INFORMAÇÕES
    # =========================
    infos = ft.Column(
        spacing=5,
        controls=[
            ft.Row(
                wrap=True,
                controls=[
                    ft.Text(
                        "Data que foi encontrado:",
                        weight=ft.FontWeight.BOLD,
                        size=12
                    ),

                    ft.Text(
                        "24/03/26 (hoje)",
                        size=12
                    )
                ]
            ),

            ft.Column(
                spacing=2,
                controls=[
                    ft.Text(
                        "Local exato:",
                        weight=ft.FontWeight.BOLD,
                        size=12
                    ),

                    ft.Text(
                        "Parque da Jaqueira, Recife PE "
                        "(em frente à igreja branca)",
                        size=12,
                    )
                ]
            ),

            ft.Row(
                wrap=True,
                controls=[
                    ft.Text(
                        "Horário:",
                        weight=ft.FontWeight.BOLD,
                        size=12
                    ),

                    ft.Text(
                        "16h:12",
                        size=12
                    )
                ]
            ),
        ]
    )

    # =========================
    # DESCRIÇÃO
    # =========================
    descricao = ft.Text(
        "Golden encontrado no Parque da Jaqueira. "
        "Muito dócil e bem treinado, responde ao "
        "comando como: “Senta”, “Me dá a patinha”.",
        size=18,
        weight=ft.FontWeight.W_500,
    )

    # =========================
    # RESPONSIVIDADE
    # =========================
    mobile = page.width < 600

    # =========================
    # IMAGENS PC
    # =========================
    imagens_pc = ft.Row(
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
    )

    # =========================
    # IMAGENS CELULAR
    # =========================
    imagens_mobile = ft.Column(
        spacing=10,
        controls=[
            ft.Container(
                border_radius=15,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                content=ft.Image(
                    src="https://placedog.net/300/250?id=1",
                    width=300,
                    height=220,
                )
            ),

            ft.Container(
                border_radius=15,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                content=ft.Image(
                    src="https://placedog.net/300/250?id=2",
                    width=300,
                    height=220,
                )
            ),
        ]
    )

    # =========================
    # BOTÃO
    # =========================
    botao = ft.ElevatedButton(
        "Contatar anunciante",
        bgcolor="#74d3b0",
        color="white",

        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=20,
        ),

        width=300 if mobile else None
    )

    # =========================
    # CONTEÚDO RESPONSIVO
    # =========================
    conteudo = ft.Column(
        spacing=15,
        controls=[
            topo,
            infos,
            descricao,

            imagens_mobile if mobile else imagens_pc,

            ft.Row(
                alignment=(
                    ft.MainAxisAlignment.CENTER
                    if mobile
                    else ft.MainAxisAlignment.END
                ),
                controls=[botao]
            )
        ]
    )

    # =========================
    # CARD
    # =========================
    post = ft.Container(
        width=350 if mobile else 600,
        bgcolor="white",
        border_radius=20,
        padding=20,

        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 4),
        ),

        content=conteudo
    )

    # =========================
    # PAGE
    # =========================
    page.add(

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