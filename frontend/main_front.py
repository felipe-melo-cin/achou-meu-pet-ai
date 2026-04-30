# verificar integração do main.py (front e back)
import flet as ft
from screens.tela_inicial import tela_inicial

def main(page: ft.Page):
    
    # minhas fontes
    page.fonts = {
        "ABeeZee": "fonts/ABeeZee-Regular.ttf",
        "LeagueLight": "fonts/LeagueSpartan-Light.ttf",
        "LeagueMedium": "fonts/LeagueSpartan-Medium.ttf"
    }

    page.title = "Achou meu Pet AI"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Centralização garantida na página
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    tela_inicial(page)



ft.run(main)