import flet as ft


def tela_matches(page: ft.Page):

    def abrir_post(e):
        
        from frontend.screens.tela_post_animal import tela_post_animal
        tela_post_animal(page)

    def criar_card(nome, tempo):
        return ft.Container(
            width=180,
            height=220,
            bgcolor="white",
            border_radius=15,
            padding=10,
            on_click=abrir_post,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src="https://placedog.net/200/200"),
                    ft.Text("Perdido"),
                    ft.Text(nome),
                    ft.Text(tempo),
                ]
            )
        )

    page.clean()

    page.add(
        ft.Text("Animais encontrados", size=24),

        ft.Row(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                criar_card("Recife - PE", "5m atrás"),
                criar_card("Olinda - PE", "2d atrás"),
            ]
        )
    )

    page.update()